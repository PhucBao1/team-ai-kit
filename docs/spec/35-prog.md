# 35 · Kỹ thuật lập trình — Async đầu-cuối, ghi nhiều hệ thống an toàn, chịu được lỗi

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Kỹ thuật | Vấn đề giải quyết | Chỗ dùng |
| --- | --- | --- |
| **Async đầu-cuối** (FastAPI async, httpx.AsyncClient, asyncpg) | Agent chủ yếu chờ I/O (model, tool, DB); thread chặn làm tốn instance | Toàn bộ API, agent, MCP |
| **Gọi tool song song có timeout** (asyncio.TaskGroup) | Tra xe, kho, slot tuần tự → chậm | find_options, context builder |
| **Streaming SSE + huỷ khi client ngắt** | Khách đóng app mà model vẫn chạy → tốn tiền | /chat |
| **Retry có backoff + jitter, circuit breaker, bulkhead** | Hệ thống gốc chập chờn kéo sập cả agent | Mọi MCP server; mỗi hệ thống gốc một pool riêng |
| **Idempotency key** | Retry tạo lịch trùng | Mọi tool ghi |
| **Transactional outbox** | Ghi DB thành công nhưng gửi sự kiện thất bại (dual-write) | Journey, promise, audit → Pub/Sub |
| **Saga + hành động bù** | Đổi lịch = giữ linh kiện mới + đặt slot mới + trả slot cũ trên 2–3 hệ thống | reschedule, lập lại phương án UC3 |
| **Optimistic locking** (cột version) | NV và agent cùng sửa một lệnh sửa chữa | appointments, repair_orders |
| **Khoá tạm có TTL** (Redis) | Hai khách được đề xuất cùng một slot | Khoá slot 15 phút khi đưa phương án |
| **Rate limit token bucket** | Làn sóng tin chủ động; lạm dụng API | Arbitration, API gateway |
| **Hexagonal (ports & adapters)** | Đổi hệ thống giả lập ↔ hệ thống thật không đụng logic | tools/ là adapter; core/ là domain |
| **Feature flag** | Bật tự động hoá theo loại hành động, theo xưởng, theo % | Làn 2, canary |

```python
# Gọi song song có timeout — context builder
async def build_context(vin: str, appt_id: str) -> Context:
    async with asyncio.timeout(2.5):                       # ngân sách thời gian cho cả bước
        async with asyncio.TaskGroup() as tg:
            veh   = tg.create_task(vehicle.status(vin))
            stock = tg.create_task(parts.stock_near(vin))
            slots = tg.create_task(service.free_slots(vin, days=7))
    return Context(vehicle=veh.result(), stock=stock.result(), slots=slots.result())

# Saga: đổi lịch trên 3 hệ thống, bù nếu bước sau lỗi
async def reschedule_saga(old, opt, key):
    done = []
    try:
        r = await parts.reserve(opt.part, opt.ws, idem=f"{key}:reserve"); done.append(("reserve", r))
        a = await service.book(opt.slot, idem=f"{key}:book");            done.append(("book", a))
        await service.cancel(old.id, idem=f"{key}:cancel_old")
        await outbox.add("appointment.rescheduled", {"old": old.id, "new": a.id})
    except Exception:
        for step, obj in reversed(done):                               # hành động bù
            await COMPENSATE[step](obj, idem=f"{key}:undo:{step}")
        raise

# Transactional outbox: ghi DB và sự kiện trong cùng transaction
async with db.begin() as tx:
    await tx.execute(update_promise(...))
    await tx.execute(insert_outbox(type="promise.updated", payload=...))
# worker riêng đọc outbox → publish Pub/Sub → đánh dấu đã gửi (at-least-once, consumer idempotent)
```
