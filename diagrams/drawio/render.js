// node render.js in.drawio out.drawio.svg out.png
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [inp,outSvg,outPng]=process.argv.slice(2);const xml=fs.readFileSync(inp,'utf8');
const b=await chromium.launch();const p=await b.newPage({viewport:{width:2000,height:1400},deviceScaleFactor:1});
const logs=[];p.on('console',m=>logs.push(m.text()));p.on('pageerror',e=>logs.push('ERR '+e.message));
await p.goto('http://127.0.0.1:8765/render.html');
const res=await p.evaluate((xml)=>{
  const doc=mxUtils.parseXml(xml);
  const diagram=doc.documentElement.getElementsByTagName('diagram')[0];
  const model=diagram.getElementsByTagName('mxGraphModel')[0];
  const div=document.getElementById('c');
  const graph=new Graph(div);graph.setEnabled(false);
  const codec=new mxCodec(model.ownerDocument);codec.decode(model,graph.getModel());
  const svgRoot=graph.getSvg('#ffffff',1,20,false,null,true,null,null,null,false,null,'light');
  svgRoot.setAttribute('content',xml);
  const s=new XMLSerializer().serializeToString(svgRoot);
  return {s, w:svgRoot.getAttribute('width'), h:svgRoot.getAttribute('height')};
},xml);
fs.writeFileSync(outSvg,res.s);
const p2=await b.newPage({viewport:{width:parseInt(res.w)+10,height:parseInt(res.h)+10}});
await p2.goto('file://'+require('path').resolve(outSvg));await p2.screenshot({path:outPng});
console.log('size',res.w,res.h);console.log(logs.slice(0,10).join('\n'));await b.close();})();
