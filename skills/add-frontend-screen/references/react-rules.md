# Luật React / Vite / TanStack Query cho frontend P-073

Đọc khi viết hook, state, component dùng chung, hoặc khi thấy mình gõ `useEffect`. Luật nhóm; thắng gợi ý từ nguồn ngoài.

## Phiên bản
- Đọc `frontend/package.json` trước: React 18 hay 19. Bản 18 → KHÔNG dùng API chỉ có ở 19 (`use()`, `useActionState`,
  `useOptimistic`, `ref` như prop thường, `<Context>` làm provider, form actions). Bản 19 → không cần `forwardRef` cho component mới.
- TypeScript strict; không `any`, không `as` để ép kiểu dữ liệu API (kiểu lấy từ `src/api/types.ts`).

## State và render
1. **Giá trị dẫn xuất tính ngay khi render**, không `useEffect` + `setState` để đồng bộ
   (`const overdue = jobs.filter(isOverdue)`; tốn kém thật mới `useMemo`).
2. **Phản ứng với hành động của người dùng trong event handler**, không qua effect theo dõi state. `useEffect` chỉ để đồng bộ với
   hệ thống ngoài (SSE, `matchMedia`, tiêu đề trang) và luôn có cleanup.
3. **Không định nghĩa component bên trong component** (mỗi lần render tạo kiểu mới → mất state, mất focus của ô nhập). Đưa ra ngoài
   hoặc thành hàm render thường.
4. **Render có điều kiện**: `cond ? <X /> : null`, không `count && <X />` (in ra số `0`).
5. `setState` phụ thuộc giá trị cũ → dạng hàm `setN(n => n + 1)`. Khởi tạo tốn kém → `useState(() => init())`.
6. Danh sách: `key` là id ổn định từ dữ liệu, không dùng index khi danh sách đổi thứ tự.

## Server state
7. **Dữ liệu server chỉ ở TanStack Query** (`useQuery` / `useMutation` trong `src/api/`). Store giao diện (Zustand / context) không
   chứa bản sao jobs, handoffs, tin nhắn. Cần dữ liệu ở nơi khác → gọi lại cùng hook (Query tự gộp request).
8. `queryKey` dạng mảng có tham số (`['jobs', vehicleId]`); mutation xong → `invalidateQueries` đúng key. Cập nhật lạc quan cho
   Xác nhận: lưu snapshot, hoàn tác trong `onError`, không hiện "đã đặt" trước `onSuccess`.
9. Mỗi mutation ghi gửi kèm idempotency key sinh 1 lần cho mỗi lần bấm (giữ trong ref), để bấm lại / mạng chập chờn không gửi lặp.

## Component dùng chung
10. **Biến thể rõ ràng thay vì nhiều boolean prop**: `<JobCard variant="customer" />` / `variant="staff"` hoặc tách
    `CustomerJobCard`, `StaffJobCard` dùng chung phần con — không `<JobCard isStaff isCompact showActions hideFooter />`.
11. Component phức tạp (thẻ handoff, khung chat) → ghép từ phần con (`HandoffCard.Header`, `.Actions`) hoặc `children`,
    không render-prop lồng nhau.

## Trình duyệt và bảo mật
12. **localStorage** chỉ cho tuỳ chọn giao diện (theme, panel thu gọn): khoá có version (`p073:theme:v1`), đọc / ghi trong
    `try/catch` (chế độ riêng tư, hết dung lượng), trả mặc định khi lỗi. KHÔNG lưu PII, token xác nhận, token đăng nhập, nội dung chat.
13. Không barrel import nặng: import đúng file (`lucide-react` theo từng icon có tree-shaking; tránh `import * as`); không tạo
    `index.ts` gom mọi thứ trong `src/components/`. Màn lớn tách bằng `React.lazy` theo route.
14. **Vite**: `build.sourcemap: 'hidden'` (có map để debug, không lộ cho trình duyệt); biến môi trường chỉ qua `import.meta.env.VITE_*`
    và không chứa secret. Không thêm `<script>` / stylesheet từ CDN bên thứ ba (phông, analytics, widget) — tự host hoặc ADR.
15. Lỗi render của một màn không làm trắng cả app: bọc mỗi màn bằng error boundary hiện thông báo tiếng Việt + "Thử lại".

---
Ý tưởng tham khảo từ `react-best-practices` và `composition-patterns` của vercel-labs/agent-skills
(https://github.com/vercel-labs/agent-skills, MIT) — chỉ rút ý, viết lại bằng lời của nhóm; không chép nội dung.
