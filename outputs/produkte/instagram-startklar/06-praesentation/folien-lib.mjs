// Gemeinsame Folien-Bausteine fuer die Startklar-Lektionsdecks (Stil = Modul 1).
import pptxgen from "pptxgenjs";
export const P = { petrol:"2F6F6F", blau:"1E3A4C", orange:"D6832F", creme:"F1ECDD",
  text:"33413F", weiss:"FFFFFF", muted:"7A8B88", tint:"EAF1F0" };
const HEAD="Cambria", BODY="Calibri", W=13.3, H=7.5, MX=0.75;

export function deck(){
  const pres = new pptxgen();
  pres.defineLayout({ name:"MLB", width:W, height:H });
  pres.layout = "MLB";
  const notes=(s,t)=>{ if(t) s.addNotes(t); };
  function phoneIcon(s,x,y,h,col){ const w=h*0.52;
    s.addShape(pres.ShapeType.roundRect,{x,y,w,h,rectRadius:0.06,fill:{color:col},line:{type:"none"}});
    s.addShape(pres.ShapeType.roundRect,{x:x+w*0.12,y:y+h*0.13,w:w*0.76,h:h*0.62,rectRadius:0.02,fill:{color:P.weiss},line:{type:"none"}});
    s.addShape(pres.ShapeType.ellipse,{x:x+w*0.42,y:y+h*0.83,w:w*0.16,h:w*0.16,fill:{color:P.weiss},line:{type:"none"}}); }
  function chip(s,x,y,txt,fill,tcol,w){ s.addText(txt,{x,y,w:w||2.4,h:0.42,isTextBox:true,shape:pres.ShapeType.roundRect,rectRadius:0.09,
    fill:{color:fill},color:tcol,fontFace:BODY,fontSize:12,bold:true,align:"center",valign:"middle",charSpacing:2,margin:0}); }

  const api = {
    pres,
    modultitel(d){ const s=pres.addSlide(); s.background={color:P.blau};
      s.addText(d.kicker,{x:MX,y:2.2,w:W-2*MX,h:0.5,isTextBox:true,color:P.orange,fontFace:BODY,fontSize:16,bold:true,charSpacing:4});
      s.addText(d.title,{x:MX,y:2.7,w:W-2*MX,h:1.5,isTextBox:true,color:P.weiss,fontFace:HEAD,fontSize:54,bold:true});
      s.addText(d.sub,{x:MX,y:4.25,w:W-2*MX,h:0.6,isTextBox:true,color:P.creme,fontFace:BODY,fontSize:20,italic:true}); notes(s,d.note); },
    titel(d){ const s=pres.addSlide(); s.background={color:P.weiss};
      s.addText(d.num,{x:9.2,y:0.4,w:3.6,h:3.2,isTextBox:true,color:P.tint,fontFace:HEAD,fontSize:200,bold:true,align:"right",valign:"top",margin:0});
      chip(s,MX,0.85,"LEKTION "+d.lekt,P.petrol,P.weiss,2.1);
      s.addText(d.title,{x:MX,y:1.7,w:8.6,h:2.6,isTextBox:true,color:P.blau,fontFace:HEAD,fontSize:38,bold:true,valign:"top"});
      if(d.sub) s.addText(d.sub,{x:MX,y:4.5,w:9.2,h:1.6,isTextBox:true,color:P.muted,fontFace:BODY,fontSize:19,italic:true,valign:"top"}); notes(s,d.note); },
    lernen(d){ const s=pres.addSlide(); s.background={color:P.weiss};
      s.addText("WAS DU LERNEN WIRST",{x:MX,y:0.75,w:W-2*MX,h:0.5,isTextBox:true,color:P.petrol,fontFace:BODY,fontSize:16,bold:true,charSpacing:3});
      let y=2.0; d.items.forEach((t,i)=>{ s.addShape(pres.ShapeType.ellipse,{x:MX,y,w:0.62,h:0.62,fill:{color:P.orange},line:{type:"none"}});
        s.addText(String(i+1),{x:MX,y,w:0.62,h:0.62,isTextBox:true,color:P.weiss,fontFace:HEAD,fontSize:22,bold:true,align:"center",valign:"middle",margin:0});
        s.addText(t,{x:MX+0.95,y:y-0.05,w:W-2*MX-1.1,h:0.9,isTextBox:true,color:P.text,fontFace:BODY,fontSize:20,valign:"middle"}); y+=1.25; }); notes(s,d.note); },
    inhalt(d){ const s=pres.addSlide(); s.background={color:P.weiss};
      s.addText(d.header.toUpperCase(),{x:MX,y:0.75,w:W-2*MX,h:0.5,isTextBox:true,color:P.petrol,fontFace:BODY,fontSize:16,bold:true,charSpacing:3});
      if(d.title) s.addText(d.title,{x:MX,y:1.3,w:W-2*MX,h:1.0,isTextBox:true,color:P.blau,fontFace:HEAD,fontSize:34,bold:true});
      let y=d.title?2.6:1.9; d.items.forEach((it,i)=>{ if(it.num){ s.addShape(pres.ShapeType.ellipse,{x:MX,y,w:0.55,h:0.55,fill:{color:P.petrol},line:{type:"none"}});
          s.addText(String(i+1),{x:MX,y,w:0.55,h:0.55,isTextBox:true,color:P.weiss,fontFace:HEAD,fontSize:20,bold:true,align:"center",valign:"middle",margin:0}); }
        const tx=it.num?MX+0.9:MX; const runs=[]; if(it.label) runs.push({text:it.label+"  ",options:{bold:true,color:P.orange}}); if(it.text) runs.push({text:it.text,options:{color:P.text}});
        s.addText(runs,{x:tx,y:y-0.05,w:W-tx-MX,h:it.big?1.2:0.85,isTextBox:true,fontFace:BODY,fontSize:it.big?22:19,valign:"middle"}); y+=it.big?1.35:1.0; });
      if(d.foot) s.addText(d.foot,{x:MX,y:H-1.1,w:W-2*MX,h:0.6,isTextBox:true,color:P.muted,fontFace:BODY,fontSize:15,italic:true}); notes(s,d.note); },
    zitat(d){ const s=pres.addSlide(); s.background={color:P.weiss};
      s.addText(d.header.toUpperCase(),{x:MX,y:0.85,w:W-2*MX,h:0.5,isTextBox:true,color:P.petrol,fontFace:BODY,fontSize:16,bold:true,charSpacing:3});
      s.addText(d.quote,{x:MX,y:2.1,w:W-2*MX,h:2.0,isTextBox:true,color:P.blau,fontFace:HEAD,fontSize:32,bold:true,italic:true,valign:"top"});
      if(d.sub) s.addText(d.sub,{x:MX,y:4.7,w:W-2*MX,h:1.2,isTextBox:true,color:P.text,fontFace:BODY,fontSize:19,valign:"top"}); notes(s,d.note); },
    handy(d){ const s=pres.addSlide(); s.background={color:P.blau}; phoneIcon(s,MX,0.8,1.15,P.orange);
      s.addText("JETZT AM HANDY MIT",{x:MX+1.0,y:0.8,w:W-2*MX-1.0,h:0.6,isTextBox:true,color:P.orange,fontFace:BODY,fontSize:20,bold:true,charSpacing:3,valign:"middle"});
      s.addText(d.sub,{x:MX+1.0,y:1.35,w:W-2*MX-1.0,h:0.6,isTextBox:true,color:P.creme,fontFace:BODY,fontSize:18,italic:true,valign:"middle"});
      let y=2.5; d.steps.forEach((t,i)=>{ s.addText(String(i+1),{x:MX,y,w:0.5,h:0.5,isTextBox:true,color:P.blau,fill:{color:P.creme},fontFace:HEAD,fontSize:16,bold:true,align:"center",valign:"middle",shape:pres.ShapeType.ellipse,margin:0});
        s.addText(t,{x:MX+0.8,y:y-0.05,w:W-MX-0.8-MX,h:0.7,isTextBox:true,color:P.weiss,fontFace:BODY,fontSize:16.5,valign:"middle"}); y+=Math.max(0.7,0.55+(t.length>70?0.3:0)); }); notes(s,d.note); },
    aufgabe(d){ const s=pres.addSlide(); s.background={color:P.weiss};
      s.addShape(pres.ShapeType.roundRect,{x:MX,y:1.5,w:W-2*MX,h:4.3,rectRadius:0.12,fill:{color:P.tint},line:{type:"none"}});
      s.addText("DEINE AUFGABE",{x:MX+0.6,y:2.0,w:W-2*MX-1.2,h:0.5,isTextBox:true,color:P.orange,fontFace:BODY,fontSize:17,bold:true,charSpacing:3});
      s.addText(d.text,{x:MX+0.6,y:2.6,w:W-2*MX-1.2,h:1.8,isTextBox:true,color:P.blau,fontFace:HEAD,fontSize:26,bold:true,valign:"top"});
      chip(s,MX+0.6,4.85,"WERKSTATT · Station „"+d.station+"“",P.orange,P.weiss,4.6); notes(s,d.note); },
    ausblick(d){ const s=pres.addSlide(); s.background={color:P.weiss};
      s.addText("ALS NÄCHSTES",{x:MX,y:2.7,w:W-2*MX,h:0.5,isTextBox:true,color:P.petrol,fontFace:BODY,fontSize:16,bold:true,charSpacing:3});
      s.addText(d.text,{x:MX,y:3.25,w:W-2*MX,h:1.6,isTextBox:true,color:P.blau,fontFace:HEAD,fontSize:30,bold:true,valign:"top"}); notes(s,d.note); },
    abschluss(d){ const s=pres.addSlide(); s.background={color:P.blau};
      chip(s,MX,0.9,d.kicker||"ABGESCHLOSSEN",P.orange,P.weiss,3.8);
      s.addText(d.title,{x:MX,y:1.7,w:W-2*MX,h:1.2,isTextBox:true,color:P.weiss,fontFace:HEAD,fontSize:46,bold:true});
      s.addText(d.text,{x:MX,y:3.1,w:W-2*MX,h:1.6,isTextBox:true,color:P.creme,fontFace:BODY,fontSize:20,valign:"top"});
      if(d.station) chip(s,MX,5.0,"WERKSTATT · Station „"+d.station+"“",P.petrol,P.weiss,4.6); notes(s,d.note); },
  };
  return api;
}
