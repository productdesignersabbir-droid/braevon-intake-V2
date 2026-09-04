
(function(){
  var stage=document.getElementById('stage');
  var steps=[].slice.call(stage.querySelectorAll('.step'));
  var prog=document.getElementById('prog');
  var segs=[].slice.call(prog.querySelectorAll('.seg span'));
  var backBtn=document.getElementById('backBtn');
  var dq=document.getElementById('dq'), done=document.getElementById('done');
  var dqFallback=null;
  function stop(on, reason){
    var slot=dq.querySelector('[data-dq-reason]');
    if(slot){
      if(dqFallback===null) dqFallback=slot.textContent;
      slot.textContent = (on && reason) ? reason : dqFallback;
    }
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
     - ANY open follow-up holds the screen, optional or not. Optional means it
       does not gate Next - the patient can move on without typing - and that
       is a different thing from letting the screen leave on its own while the
       box is sitting there open. Answering "Yes" is what opens the box, so
       auto-advancing on that same click took the box away as it arrived;
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
    if(el.querySelector('.reveal.on')) return;
    if(!stepValid(el)) return;
    setTimeout(function(){ if(steps[idx]===el) advance(); }, 140);
  }

  /* ------------------------------------------------------------ reveals */
  function syncReveals(){
    [].forEach.call(stage.querySelectorAll('.reveal[data-reveal-for]'), function(r){
      var g=r.dataset.revealFor, on=r.dataset.revealOn, picked=sel(g);
      var none=r.dataset.revealNone || 'none';
      var show = on==='*'
        ? picked.some(function(v){ return v!==none; })
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

  /* --------------------------------------------------- empty select state */
  /* A select whose placeholder option is showing has to read as a placeholder,
     not as an answer already given - the reference greys its own the same way.
     Marked as an attribute rather than a :has() rule so it works everywhere. */
  function markEmpty(f){
    if(f && f.tagName==='SELECT') f.toggleAttribute('data-empty', !f.value);
  }
  [].forEach.call(stage.querySelectorAll('select'), markEmpty);
  stage.addEventListener('change', function(e){ markEmpty(e.target); });

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
  /* What is wrong with a field, in words, or null if nothing is. Shared by the
     validity check and the error display so the two cannot disagree. */
  function fieldProblem(f){
    if(f.closest('[data-optional]')) return null;
    if(!f.value.trim()) return 'This field is required.';
    if(f.hasAttribute('data-us-phone') && !usValid(f.value))
      return 'Enter a valid US phone number, e.g. (415) 555-1234.';
    if(f.type==='email' && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(f.value.trim()))
      return 'Enter a valid email address.';
    return null;
  }

  function stepValid(el){
    var ok=true;
    [].forEach.call(el.querySelectorAll('.opts'), function(box){
      if(box.dataset.optional) return;
      if(box.closest('.reveal') && !box.closest('.reveal').classList.contains('on')) return;
      if(!box.querySelector('.opt.selected')) ok=false;
    });
    [].forEach.call(el.querySelectorAll('.field input, .field select'), function(f){
      if(fieldProblem(f)) ok=false;
    });
    [].forEach.call(el.querySelectorAll('.reveal.on:not([data-optional]) textarea'), function(t){
      if(!t.value.trim()) ok=false;
    });
    return ok;
  }
  function showError(el){
    var r=el.querySelector('.reveal.on .err');
    if(r) r.hidden=false;
    /* Say what is wrong, under the field it is wrong in. */
    var firstBad=null;
    [].forEach.call(el.querySelectorAll('.field input, .field select'), function(f){
      var why=fieldProblem(f), box=f.closest('.field'), msg=box&&box.querySelector('.err');
      box.classList.toggle('bad', !!why);
      if(msg){ msg.textContent = why || ''; msg.hidden = !why; }
      if(why && !firstBad) firstBad=f;
    });
    var first=firstBad || el.querySelector('.opts:not([data-optional]) , .field input, .field select');
    if(first) first.scrollIntoView({block:'center', behavior:'smooth'});
    if(firstBad) try{ firstBad.focus({preventScroll:true}); }catch(_){}
    el.animate([{transform:'translateX(0)'},{transform:'translateX(-5px)'},
                {transform:'translateX(5px)'},{transform:'translateX(0)'}],
               {duration:220});
  }
  function clearError(el){ if(!el) return;
    [].forEach.call(el.querySelectorAll('.err'), function(e){ e.hidden=true; });
    [].forEach.call(el.querySelectorAll('.field.bad'), function(b){
      b.classList.remove('bad'); }); }

  stage.addEventListener('input', function(e){
    if(!e.target.matches('input,select,textarea')) return;
    var box=e.target.closest('.field');
    if(box && !fieldProblem(e.target)){
      box.classList.remove('bad');
      var m=box.querySelector('.err'); if(m) m.hidden=true;
    }
    clearError(e.target.closest('.step'));
  });

  /* --------------------------------------------------- disqualification */
  function disqualifies(el){
    /* `data-dq-on` is the list of answers that stop the flow on this screen.
       The reference writes its rules two ways and the extractor flattens both
       into that list: one named answer ("Never", "More than 3 years ago"), or
       everything except the exclusive "None of these" on a safety screen. */
    var reason=el.dataset.dq; if(!reason) return null;
    var named=el.hasAttribute('data-dq-on');
    var stop=(el.dataset.dqOn||'').split('|');
    /* No named answers means the screen stops on ANY answer but its "none of
       these" - v1's nitrate screen, where every option is a contraindication.
       `data-dq-safe` carries that one exempt value. Without this branch such a
       screen has a reason nothing can ever trigger. */
    var safe=el.dataset.dqSafe;
    var hit=false;
    [].forEach.call(el.querySelectorAll('.opts'), function(box){
      var rev=box.closest('.reveal');
      if(rev && !rev.classList.contains('on')) return;
      [].forEach.call(box.querySelectorAll('.opt.selected'), function(o){
        var v=o.dataset.value;
        if(named ? stop.indexOf(v)>-1 : v!==safe) hit=true;
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
    /* The whole nav row goes, not just its contents - hiding the bar and the
       back arrow individually left the row's own height behind, which is the
       gap that showed above the review header. */
    var navrow = document.querySelector('.navrow');
    if(navrow) navrow.hidden = bare;
    if(bare) prog.hidden = true;
    backBtn.hidden = bare || el.hasAttribute('data-no-back') || history.length===0;
    window.scrollTo({top:0, behavior:'auto'});
    if(el.querySelector('[data-loader]')) runLoader(el);
    if(el.querySelector('[data-name-echo],[data-echo],[data-fname-echo]')) fillSummary(el);
    if(el.hasAttribute('data-checkout')) startClock(el);
    echoState();
  }

  /* ------------------------------------------------- the checkout's clock */
  /* One interval and one deadline, painted onto every [data-countdown] on the
     screen - the reference states the same time in three places and they must
     not disagree. It starts when the checkout is first reached rather than on
     load, so the time cannot have run down while the questionnaire was being
     filled in; walking back and forward again picks the running clock up rather
     than restarting it, because a deadline that resets on every visit reads as
     a trick. At zero it holds at 00:00 - nothing on this page is withdrawn. */
  var CLOCK_SECS=600, clockLeft=CLOCK_SECS, clockTimer=null;
  function paintClock(el){
    var m=Math.floor(clockLeft/60), s=clockLeft%60;
    var t=m+':'+(s<10?'0':'')+s;
    [].forEach.call(el.querySelectorAll('[data-countdown]'), function(b){
      b.textContent=t;
    });
  }
  function startClock(el){
    paintClock(el);
    if(clockTimer) return;
    clockTimer=setInterval(function(){
      if(clockLeft<=0){ clearInterval(clockTimer); clockTimer=null; return; }
      clockLeft--; paintClock(el);
    }, 1000);
  }

  /* ------------------------------------------------- the checkout's packs */
  /* The price lives on the card as `data-price`, so there is one place to edit
     it and the rendered figure is never the source of truth. The static frames
     run no script and show the pack `checkout.LEAD_PACK` names, which is the
     one that opens selected here too. */
  stage.addEventListener('click', function(e){
    var pack=e.target.closest('.ck-pack'); if(!pack) return;
    var box=pack.closest('[data-packs]'); if(!box) return;
    [].forEach.call(box.querySelectorAll('.ck-pack'), function(p){
      p.classList.remove('selected');
    });
    pack.classList.add('selected');
    var card=pack.closest('.step');
    var tag=card.querySelector('[data-pack-tag]');
    var price=card.querySelector('[data-pack-price]');
    if(tag) tag.textContent=pack.dataset.pack+' PACK';
    if(price) price.textContent=pack.dataset.price;
  });
  function advance(){
    var el=steps[idx];
    if(!stepValid(el)){ showError(el); return; }
    var why=disqualifies(el);
    if(why){ stop(true, why); return; }
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
    /* The checkout's headline and its clock bar both open on the patient's
       name in the possessive - "Marcus's approval is valid for". A separate
       hook from [data-name-echo] because that one carries a whole clause. */
    [].forEach.call(el.querySelectorAll('[data-fname-echo]'), function(e){
      e.textContent = (fn&&fn.value.trim()) ? fn.value.trim()+'\u2019s' : 'Your';
    });
    /* The goals card leads its echoed line with that goal's own glyph. All
       five ship inside the span; this shows the one the answer names and hides
       the rest. With no answer the markup's own `on` stays put, which is what
       the JS-less frames render. */
    [].forEach.call(el.querySelectorAll('[data-echo-icon]'), function(e){
      /* `label()` joins a multi-answer screen's picks with ", ", and v1's goals
         question is multi - so match the FIRST goal picked rather than the
         whole string, or nothing matches and the chip renders no icon. */
      var want=(label(e.dataset.echoIcon)||'').split(', ')[0];
      if(!want) return;
      [].forEach.call(e.children, function(i){
        i.classList.toggle('on', i.dataset.goal===want);
      });
    });
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
