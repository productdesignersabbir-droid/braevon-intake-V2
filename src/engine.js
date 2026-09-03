
(function(){
  var stage=document.getElementById('stage');
  var steps=[].slice.call(stage.querySelectorAll('.step'));
  var prog=document.getElementById('prog');
  var segs=[].slice.call(prog.querySelectorAll('.seg span'));
  var backBtn=document.getElementById('backBtn');
  var dq=document.getElementById('dq'), done=document.getElementById('done');
  function stop(on){
    dq.classList.toggle('on', on);
    stage.hidden=on; prog.hidden=on||prog.hidden; backBtn.hidden=on||backBtn.hidden;
  }
  var TOTAL_Q=__TOTAL_Q__, SEGMENTS=__SEGMENTS__;
  /* The bar is divided by section, not by question count - see build.py. */
  var SEGMENT_STARTS=__SEGMENT_STARTS__, STEP_AT=__STEP_AT__;
  function segmentOf(screen){
    var step=STEP_AT[screen]||1, at=0;
    SEGMENT_STARTS.forEach(function(start,i){ if(step>=start) at=i; });
    return at;
  }
  var answers={};      /* group -> array of selected values */
  var idx=0, history=[];
  /* progQ[j] is the question number the bar should show on step j - its own if
     it is a question, otherwise the last one before it. */
  var progQ=(function(){ var out=[], last=0;
    steps.forEach(function(s,j){ var v=s.dataset.q?+s.dataset.q:0; if(v) last=v; out[j]=last; });
    return out; })();

  /* ---------------------------------------------------------- selection */
  function sel(group){ return answers[group]||[]; }

  stage.addEventListener('click', function(e){
    var opt=e.target.closest('.opt'); if(!opt) return;
    var box=opt.closest('.opts'); if(!box) return;
    var group=box.dataset.group, multi=box.dataset.mode==='multi';
    var val=opt.dataset.value;

    if(!multi){
      [].forEach.call(box.querySelectorAll('.opt'), function(o){ o.classList.remove('selected'); });
      opt.classList.add('selected');
      answers[group]=[val];
      if(opt.dataset.sys) setBP(opt.dataset.sys, opt.dataset.dia, false);
    } else {
      var on=!opt.classList.contains('selected');
      opt.classList.toggle('selected', on);
      /* "None of these" is exclusive both ways: picking it clears the rest,
         and picking anything else clears it. */
      if(on && opt.dataset.exclusive){
        [].forEach.call(box.querySelectorAll('.opt'), function(o){
          if(o!==opt) o.classList.remove('selected'); });
      } else if(on){
        [].forEach.call(box.querySelectorAll('.opt[data-exclusive]'), function(o){
          o.classList.remove('selected'); });
      }
      answers[group]=[].map.call(box.querySelectorAll('.opt.selected'),
                                function(o){ return o.dataset.value; });
    }
    syncReveals(); clearError(opt.closest('.step'));
    maybeAutoAdvance(opt, multi);
  });

  /* Answering advances the screen; Continue stays and still works, so this is
     a shortcut past it rather than a replacement. Four things hold it back:

     - a multi-select waits, unless the answer is the exclusive "None of these"
       — on "select all that apply" the patient may well want two or three, and
       leaving on the first tick collects exactly one;
     - unticking never advances;
     - an open follow-up still has to be typed into;
     - the blood-pressure screen never jumps: picking a band fills both numbers
       and so satisfies the step, but that screen exists precisely so someone
       who knows their real reading can type it.

     Everything else is `stepValid`, which the Continue button already uses — so
     screens 4 and 28 hold on their own, their inputs being unfilled. It routes
     through `advance()`, the same function Continue calls, so a disqualifying
     answer still opens the stop screen rather than being walked past. */
  function maybeAutoAdvance(opt, multi){
    var el=steps[idx];
    if(el.querySelector('.bp')) return;
    if(multi && !opt.dataset.exclusive) return;
    if(!opt.classList.contains('selected')) return;
    if(el.querySelector('.reveal.on:not([data-optional])')) return;
    if(!stepValid(el)) return;
    setTimeout(function(){ if(steps[idx]===el) advance(); }, 140);
  }

  /* ------------------------------------------------------------ reveals */
  function syncReveals(){
    [].forEach.call(stage.querySelectorAll('.reveal[data-reveal-for]'), function(r){
      var g=r.dataset.revealFor, on=r.dataset.revealOn, picked=sel(g);
      var show = on==='*'
        ? picked.some(function(v){ return v!=='none'; })
        : picked.indexOf(on)>-1;
      r.classList.toggle('on', show);
    });
  }

  /* ------------------------------------------------------ blood pressure */
  var sysEl=stage.querySelector('[data-bp-sys]'), diaEl=stage.querySelector('[data-bp-dia]');
  var bpLead=stage.querySelector('.bp-lead'), bpWarn=stage.querySelector('[data-bp-warning]');
  function setBP(s,d,manual){
    if(!sysEl) return;
    sysEl.value=s; diaEl.value=d;
    if(bpLead) bpLead.textContent = manual
      ? 'Using the reading you entered. Pick an option above to go back to an estimate.'
      : 'Estimated from your selection. Tap a number to enter your own reading.';
    checkBP();
  }
  function checkBP(){
    if(!sysEl||!bpWarn) return;
    var s=+sysEl.value||0, d=+diaEl.value||0;
    bpWarn.classList.toggle('on', s>=160||d>=100||(s>0&&s<90)||(d>0&&d<50));
  }
  [sysEl,diaEl].forEach(function(el){
    if(!el) return;
    el.addEventListener('input', function(){
      el.value=el.value.replace(/\D/g,'');
      var box=stage.querySelector('.opts[data-group="bp"]');
      if(box){ [].forEach.call(box.querySelectorAll('.opt'),function(o){o.classList.remove('selected');});
               answers['bp']=['manual']; }
      if(bpLead) bpLead.textContent='Using the reading you entered. Pick an option above to go back to an estimate.';
      checkBP();
    });
  });

  /* ------------------------------------------------------------ US phone */
  /* Ten digits, area code and exchange both starting 2-9, which is what a real
     US number does. A leading 1 or +1 is dropped rather than rejected - people
     type it out of habit. */
  function usDigits(v){
    var d=(v||'').replace(/\D/g,'');
    if(d.length===11 && d.charAt(0)==='1') d=d.slice(1);
    return d.slice(0,10);
  }
  function usFormat(d){
    if(d.length<4) return d;
    if(d.length<7) return '('+d.slice(0,3)+') '+d.slice(3);
    return '('+d.slice(0,3)+') '+d.slice(3,6)+'-'+d.slice(6);
  }
  function usValid(v){
    var d=usDigits(v);
    return d.length===10 && /^[2-9]/.test(d) && /^[2-9]/.test(d.charAt(3));
  }
  stage.addEventListener('input', function(e){
    var f=e.target;
    if(!f.matches || !f.matches('[data-us-phone]')) return;
    var end = f.selectionStart===f.value.length;
    f.value = usFormat(usDigits(f.value));
    if(end) try{ f.setSelectionRange(f.value.length, f.value.length); }catch(_){}
  });

  /* --------------------------------------------------------- validation */
  function stepValid(el){
    var ok=true;
    [].forEach.call(el.querySelectorAll('.opts'), function(box){
      if(box.dataset.optional) return;
      if(box.closest('.reveal') && !box.closest('.reveal').classList.contains('on')) return;
      if(!box.querySelector('.opt.selected')) ok=false;
    });
    [].forEach.call(el.querySelectorAll('.field input, .field select'), function(f){
      if(f.closest('[data-optional]')) return;
      if(!f.value.trim()) ok=false;
      else if(f.hasAttribute('data-us-phone') && !usValid(f.value)) ok=false;
      else if(f.type==='email' && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(f.value.trim())) ok=false;
    });
    [].forEach.call(el.querySelectorAll('.reveal.on:not([data-optional]) textarea'), function(t){
      if(!t.value.trim()) ok=false;
    });
    return ok;
  }
  function showError(el){
    var r=el.querySelector('.reveal.on .err');
    if(r) r.hidden=false;
    var first=el.querySelector('.opts:not([data-optional]) , .field input, .field select');
    if(first) first.scrollIntoView({block:'center', behavior:'smooth'});
    el.animate([{transform:'translateX(0)'},{transform:'translateX(-5px)'},
                {transform:'translateX(5px)'},{transform:'translateX(0)'}],
               {duration:220});
  }
  function clearError(el){ if(!el) return;
    [].forEach.call(el.querySelectorAll('.err'), function(e){ e.hidden=true; }); }

  stage.addEventListener('input', function(e){
    if(e.target.matches('input,select,textarea')) clearError(e.target.closest('.step'));
  });

  /* --------------------------------------------------- disqualification */
  function disqualifies(el){
    /* `data-dq-on` is the list of answers that stop the flow on this screen.
       The reference writes its rules two ways and the extractor flattens both
       into that list: one named answer ("Never", "More than 3 years ago"), or
       everything except the exclusive "None of these" on a safety screen. */
    var reason=el.dataset.dq; if(!reason) return null;
    var stop=(el.dataset.dqOn||'').split('|');
    var hit=false;
    [].forEach.call(el.querySelectorAll('.opts'), function(box){
      [].forEach.call(box.querySelectorAll('.opt.selected'), function(o){
        if(stop.indexOf(o.dataset.value)>-1) hit=true;
      });
    });
    return hit?reason:null;
  }

  /* ------------------------------------------------------------- moving */
  function shown(el){
    /* A conditional screen names the group it depends on and the answers that
       open it. The reference branches this way six times over — one follow-up
       per ED medication tried, one per side-effect list, the two blood
       pressure readings, the A1C screen behind diabetes, and the nitrate and
       alpha-blocker follow-ups. */
    var g=el.dataset.if; if(!g) return true;
    var want=(el.dataset.ifAny||'').split('|');
    var have=sel(g);
    return want.some(function(v){ return have.indexOf(v)>-1; });
  }
  function show(i){
    loaderRun++;   /* cancel any dial still running on the screen we are leaving */
    steps.forEach(function(s,j){ s.classList.toggle('on', j===i); });
    idx=i;
    var el=steps[i];
    var q=el.dataset.q?+el.dataset.q:0, pq=progQ[i];
    prog.hidden=!pq;
    if(pq){
      prog.setAttribute('aria-valuenow', pq);
      if(q) prog.setAttribute('aria-valuetext','Question '+q+' of '+TOTAL_Q);
      else prog.removeAttribute('aria-valuetext');
      var at=segmentOf(+el.dataset.step);
      segs.forEach(function(sp,k){
        sp.style.width = k<=at ? '100%' : '0%';
        sp.parentNode.classList.toggle('now', k===at);
      });
    }
    /* The review screen carries its own result header, so the shell's masthead
       and bar step aside for it - as they do on the reference. */
    var bare = el.hasAttribute('data-bare');
    document.querySelector('.masthead').hidden = bare;
    if(bare) prog.hidden = true;
    backBtn.hidden = bare || el.hasAttribute('data-no-back') || history.length===0;
    window.scrollTo({top:0, behavior:'auto'});
    if(el.querySelector('[data-loader]')) runLoader(el);
    if(el.querySelector('[data-name-echo],[data-echo]')) fillSummary(el);
    echoState();
  }
  function advance(){
    var el=steps[idx];
    if(!stepValid(el)){ showError(el); return; }
    var why=disqualifies(el);
    if(why){ stop(true); return; }
    for(var j=idx+1;j<steps.length;j++){
      if(shown(steps[j])){ history.push(idx); show(j); return; }
    }
    /* Nothing left to show: the assessment is submitted. Without this the
       final Submit did nothing at all. */
    finish();
  }
  function finish(){
    done.classList.add('on');
    stage.hidden=true; prog.hidden=true; backBtn.hidden=true;
    window.scrollTo({top:0, behavior:'auto'});
  }
  stage.addEventListener('click', function(e){
    if(e.target.closest('.cta-next')) advance();
  });
  backBtn.addEventListener('click', function(){
    if(!history.length) return;
    show(history.pop());
  });
  document.getElementById('dqBack').addEventListener('click', function(){
    stop(false); show(idx);
  });
  document.getElementById('dqExit').addEventListener('click', function(){
    /* Exit starts the assessment over, so it has to clear the answers too -
       returning to screen 1 with the disqualifying answer still ticked is not
       a restart, it is the same dead end one Continue away. */
    [].forEach.call(stage.querySelectorAll('.opt.selected'), function(o){
      o.classList.remove('selected'); });
    [].forEach.call(stage.querySelectorAll('input,textarea'), function(f){
      if(f.type==='checkbox'||f.type==='radio') f.checked=false; else f.value=''; });
    [].forEach.call(stage.querySelectorAll('select'), function(f){ f.selectedIndex=0; });
    answers={};
    syncReveals();
    stop(false); history=[]; show(0);
  });

  /* --------------------------------------------------------------- echo */
  function echoState(){
    var s=document.getElementById('state');
    var v=s&&s.value?s.value:'your state';
    [].forEach.call(document.querySelectorAll('[data-state-echo]'), function(e){
      e.textContent=v;
    });
  }
  function label(group){
    var box=stage.querySelector('.opts[data-group="'+group+'"]');
    if(!box) return null;
    var picked=[].map.call(box.querySelectorAll('.opt.selected'), function(o){
      var l=o.querySelector('.lbl').cloneNode(true);
      var sm=l.querySelector('small'); if(sm) sm.remove();
      return l.textContent.trim();
    });
    return picked.length?picked.join(', '):null;
  }
  function fillSummary(el){
    var fn=document.getElementById('first_name');
    var n=el.querySelector('[data-name-echo]');
    /* "Marcus, how" or "How" — the sentence has to read either way, so the
       echo carries the whole opening rather than just the name. */
    if(n) n.textContent = (fn&&fn.value.trim()) ? fn.value.trim()+', how' : 'How';
    [].forEach.call(el.querySelectorAll('[data-echo]'), function(e){
      var k=e.dataset.echo;
      if(k==='bp'){
        e.textContent = (sysEl&&sysEl.value) ? sysEl.value+' / '+diaEl.value : '—';
      } else {
        e.textContent = label(k) || '—';
      }
    });
  }

  /* ------------------------------------------------------- the loaders */
  var C=2*Math.PI*58;
  var loaderRun=0;
  function runLoader(el){
    /* The processing screens carry no button: they run their dial and hand off
       on their own, the way the reference does. `loaderRun` is the guard — if
       the patient goes back mid-run, the old frame loop must not advance the
       flow out from under the screen they are now on. */
    var arc=el.querySelector('.dial-arc'), pct=el.querySelector('.pct');
    var rows=[].slice.call(el.querySelectorAll('.checklist div'));
    if(!arc) return;
    var mine=++loaderRun, from=idx, DUR=2600;
    rows.forEach(function(r){ r.classList.remove('done'); });
    arc.setAttribute('stroke-dasharray', C);

    /* The hand-off is on a timer, not on the animation frame. A background tab
       stops serving requestAnimationFrame, and this screen has no button — so
       driving the advance from the frame loop leaves anyone who switches tabs
       mid-processing stranded on a dial that never finishes. The frames are
       decoration; the timer is the flow. */
    setTimeout(function(){
      if(mine!==loaderRun || idx!==from) return;
      arc.setAttribute('stroke-dashoffset', 0);
      pct.textContent='100%';
      rows.forEach(function(r){ r.classList.add('done'); });
      setTimeout(function(){ if(mine===loaderRun && idx===from) advance(); }, 340);
    }, DUR);

    var t0=null;
    function frame(t){
      if(mine!==loaderRun) return;
      if(!t0) t0=t;
      var p=Math.min(1,(t-t0)/DUR);
      arc.setAttribute('stroke-dashoffset', C*(1-p));
      pct.textContent=Math.round(p*100)+'%';
      rows.forEach(function(r,i){ r.classList.toggle('done', p > (i+1)/(rows.length+0.6)); });
      if(p<1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  /* Two controls ship with an answer already chosen — sex on the eligibility
     screen, and "Normal" on the blood-pressure screen. Nothing clicks them, so
     without this pass the answer map starts out disagreeing with the markup and
     the summary reads them as blank. */
  [].forEach.call(stage.querySelectorAll('.opts'), function(box){
    var picked=[].map.call(box.querySelectorAll('.opt.selected'),
                           function(o){ return o.dataset.value; });
    if(picked.length) answers[box.dataset.group]=picked;
  });
  var bpPre=stage.querySelector('.opts[data-group="bp"] .opt.selected');
  if(bpPre && bpPre.dataset.sys) setBP(bpPre.dataset.sys, bpPre.dataset.dia, false);

  syncReveals();
  show(0);
})();
