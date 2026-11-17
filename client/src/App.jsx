import { useCallback, useEffect, useRef, useState } from 'react';
import { I18N, LANG_META } from './i18n.js';
import { Icon } from './icons.jsx';
import { Orb } from './orb.jsx';
import { Recorder, recordingSupported } from './recorder.js';
import SearchBox from './components/SearchBox.jsx';
import ResultView, { ApproachNav } from './components/ResultView.jsx';
import Drawer from './components/Drawer.jsx';
import VoiceSheet, { voiceStateText } from './components/VoiceSheet.jsx';

// Language option labels, exactly as in the original page.
const LANG_LABELS = {
  hinglish: 'Hinglish (हिंदी + English)',
  english: 'English',
  telugu: 'Telugu (తెలుగు)',
  tamil: 'Tamil (தமிழ்)',
  kannada: 'Kannada (ಕನ್ನಡ)',
  malayalam: 'Malayalam (മലയാളം)',
  marathi: 'Marathi (मराठी)',
  bengali: 'Bengali (বাংলা)',
  gujarati: 'Gujarati (ગુજરાતી)',
  punjabi: 'Punjabi (ਪੰਜਾਬੀ)',
};

const store = {
  get(k, d) {
    try {
      const v = localStorage.getItem(k);
      return v === null ? d : v;
    } catch (e) {
      return d;
    }
  },
  set(k, v) {
    try {
      localStorage.setItem(k, v);
    } catch (e) {
      /* storage unavailable */
    }
  },
};

// useState plus a ref that is updated synchronously, so async handlers
// and document-level listeners always read the current value (the way
// the original page's plain variables behaved).
function useStateWithRef(initial) {
  const [value, setValue] = useState(initial);
  const ref = useRef(value);
  const set = useCallback((v) => {
    const next = typeof v === 'function' ? v(ref.current) : v;
    ref.current = next;
    setValue(next);
  }, []);
  return [value, set, ref];
}

const ORB_STATUS_KEYS = {
  idle: 'orbIdle',
  listening: 'orbListening',
  thinking: 'orbThinking',
  speaking: 'orbSpeaking',
  unavailable: 'orbUnavailable',
};

export default function App() {
  const [lang, setLang, langRef] = useStateWithRef(() => {
    const saved = store.get('bolke-lang', 'hinglish');
    return LANG_META[saved] ? saved : 'hinglish';
  });
  const [theme, setTheme] = useState(() =>
    store.get('bolke-theme', 'dark') === 'light' ? 'light' : 'dark',
  );
  const [voiceAnswersOn, setVoiceAnswersOn, voiceAnswersOnRef] = useStateWithRef(
    () => store.get('bolke-voice', '1') === '1',
  );
  const [keySet, setKeySet, keySetRef] = useStateWithRef(false);
  const [languages, setLanguages] = useState(() => Object.keys(LANG_META));
  const [view, setView, viewRef] = useStateWithRef('home');
  const [currentResult, setCurrentResult, currentResultRef] = useStateWithRef(null);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [currentFocus, setCurrentFocus, currentFocusRef] = useStateWithRef('');
  const [busy, setBusy, busyRef] = useStateWithRef(false);
  const [resultLoading, setResultLoading] = useState(false);
  const [error, setError] = useState(null);
  const [orbState, setOrbStateRaw] = useState('unavailable');
  const [settingsOpen, setSettingsOpen, settingsOpenRef] = useStateWithRef(false);
  const [online, setOnline] = useState(() => navigator.onLine);
  const [isDesktop, setIsDesktop] = useState(
    () => window.matchMedia('(min-width: 1100px)').matches,
  );
  const [activeNavId, setActiveNavId] = useState('approach-0');
  // Drawer
  const [drawerMounted, setDrawerMounted, drawerMountedRef] = useStateWithRef(false);
  const [drawerOpen, setDrawerOpen, drawerOpenRef] = useStateWithRef(false);
  const [exchanges, setExchanges] = useState([]);
  const [followupBusy, setFollowupBusy, followupBusyRef] = useStateWithRef(false);
  // Voice sheet
  const [sheetMounted, setSheetMounted, sheetMountedRef] = useStateWithRef(false);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [voiceState, setVoiceStateBoth, voiceStateRef] = useStateWithRef('hidden');
  const [voiceError, setVoiceError] = useState('');
  const [voiceContext, setVoiceContext, voiceContextRef] = useStateWithRef('search');
  const [lastTranscript, setLastTranscript] = useState('');
  const [lastAnswerText, setLastAnswerText] = useState('');
  const [lastAudioBase64, setLastAudioBase64] = useState('');
  // Audio
  const [playBtn, setPlayBtn, playBtnRef] = useStateWithRef(null);
  const [playerState, setPlayerState] = useState('idle');
  const [speakBusyId, setSpeakBusyId] = useState(null);

  const playerRef = useRef(null);
  const playOnEndedRef = useRef(null);
  const livePoliteRef = useRef(null);
  const liveAssertiveRef = useRef(null);
  const orbWrapRef = useRef(null);
  const voiceOrbRef = useRef(null);
  const ampMeterRef = useRef(null);
  const recTimerRef = useRef(null);
  const searchInputRef = useRef(null);
  const resultSearchInputRef = useRef(null);
  const drawerInputRef = useRef(null);
  const threadRef = useRef(null);
  const settingsBtnRef = useRef(null);
  const settingsPopoverRef = useRef(null);
  const lastFocusedRef = useRef(null);
  const voiceReturnFocusRef = useRef(null);
  const recorderRef = useRef(null);
  const exchangeIdRef = useRef(0);
  const drawerCloseTimerRef = useRef(null);
  const sheetCloseTimerRef = useRef(null);

  const t = (k) => {
    const l = langRef.current;
    return (I18N[l] && I18N[l][k]) || I18N.english[k] || k;
  };

  function announce(msg, assertive) {
    const el = assertive ? liveAssertiveRef.current : livePoliteRef.current;
    if (!el) return;
    el.textContent = '';
    requestAnimationFrame(() => {
      el.textContent = msg;
    });
  }

  function setOrbState(state) {
    const effective = state === 'idle' && !keySetRef.current ? 'unavailable' : state;
    setOrbStateRaw(effective);
  }

  function setAmp(v) {
    const clamped = Math.max(0, Math.min(1, v));
    [orbWrapRef.current, voiceOrbRef.current, ampMeterRef.current].forEach((el) => {
      if (el) el.style.setProperty('--amp', clamped);
    });
  }

  /* ---------------- config ---------------- */
  useEffect(() => {
    let cancelled = false;
    fetch('/api/config')
      .then((r) => r.json())
      .then((cfg) => {
        if (cancelled) return;
        if (cfg && typeof cfg.key_set === 'boolean') setKeySet(cfg.key_set);
        if (cfg && Array.isArray(cfg.languages)) {
          const known = cfg.languages.filter((l) => LANG_META[l]);
          if (known.length) setLanguages(known);
        }
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setOrbState(busyRef.current ? 'thinking' : 'idle');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [keySet]);

  /* ---------------- preferences ---------------- */
  useEffect(() => {
    document.documentElement.lang = (LANG_META[lang] || LANG_META.english).bcp47;
  }, [lang]);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    store.set('bolke-theme', theme);
  }, [theme]);
  useEffect(() => {
    store.set('bolke-voice', voiceAnswersOn ? '1' : '0');
  }, [voiceAnswersOn]);

  useEffect(() => {
    const sync = () => setOnline(navigator.onLine);
    window.addEventListener('offline', sync);
    window.addEventListener('online', sync);
    return () => {
      window.removeEventListener('offline', sync);
      window.removeEventListener('online', sync);
    };
  }, []);

  useEffect(() => {
    const mq = window.matchMedia('(min-width: 1100px)');
    const fn = () => setIsDesktop(mq.matches);
    if (mq.addEventListener) mq.addEventListener('change', fn);
    return () => {
      if (mq.removeEventListener) mq.removeEventListener('change', fn);
    };
  }, []);

  /* ---------------- audio playback (one shared player) ---------------- */
  function resetPlayButton() {
    setPlayBtn(null);
  }

  function stopAudio() {
    const player = playerRef.current;
    if (!player) return;
    player.pause();
    player.removeAttribute('src');
    try {
      player.load();
    } catch (e) {
      /* nothing loaded */
    }
    resetPlayButton();
    playOnEndedRef.current = null;
    if (!busyRef.current) setOrbState('idle');
  }

  function playBase64Audio(base64, btnId, onEnded) {
    stopAudio();
    setPlayBtn(btnId || null);
    playOnEndedRef.current = onEnded || null;
    const player = playerRef.current;
    player.src = 'data:audio/mpeg;base64,' + base64;
    const p = player.play();
    if (p && p.catch) {
      p.catch(() => {
        resetPlayButton();
        setOrbState('idle');
      });
    }
  }

  function handlePlaying() {
    setPlayerState('playing');
    setOrbState('speaking');
    if (voiceStateRef.current === 'speaking' || voiceStateRef.current === 'paused') {
      setVoiceState('speaking');
    }
  }

  function handlePause() {
    const player = playerRef.current;
    if (player.ended) return;
    if (playBtnRef.current) setPlayerState('paused');
    else setPlayerState('idle');
    if (voiceStateRef.current === 'speaking') setVoiceState('paused');
    else if (!busyRef.current) setOrbState('idle');
  }

  function handleEnded() {
    resetPlayButton();
    setPlayerState('idle');
    const cb = playOnEndedRef.current;
    playOnEndedRef.current = null;
    if (voiceStateRef.current === 'speaking' || voiceStateRef.current === 'paused') {
      setVoiceState('done');
    } else if (!busyRef.current) setOrbState('idle');
    if (cb) cb();
  }

  async function speakText(text, btnId) {
    if (!keySetRef.current) {
      showError(t('voiceOffNote'));
      return;
    }
    if (btnId) setSpeakBusyId(btnId);
    try {
      const res = await fetch('/api/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, lang: langRef.current }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok || !data) throw new Error((data && data.error) || 'HTTP ' + res.status);
      const base64 = data.audio_base64 || data.audio || '';
      if (!base64) throw new Error(t('networkError'));
      playBase64Audio(base64, btnId);
    } catch (err) {
      showError(err instanceof TypeError ? t('networkError') : err.message);
    } finally {
      if (btnId) setSpeakBusyId(null);
    }
  }

  function toggleSpeak(text, btnId) {
    const player = playerRef.current;
    if (!player.paused && playBtnRef.current === btnId) {
      player.pause();
      return;
    }
    if (player.paused && playBtnRef.current === btnId && player.src) {
      player.play();
      return;
    }
    speakText(text, btnId);
  }

  /* ---------------- errors & views ---------------- */
  function showError(msg) {
    setError(msg);
    announce(t('errorTitle') + ' ' + msg, true);
  }
  function clearError() {
    setError(null);
  }
  function showHome() {
    setView('home');
    clearError();
    setOrbState('idle');
  }

  /* ---------------- search ---------------- */
  async function runSearch(question) {
    question = (question || '').trim();
    if (!question) {
      setView('result');
      showError(t('emptyQuestion'));
      return;
    }
    if (busyRef.current) return;
    setBusy(true);
    clearError();
    stopAudio();
    setCurrentQuestion(question);
    setCurrentFocus('');
    setExchanges([]);
    setView('result');
    if (resultSearchInputRef.current) resultSearchInputRef.current.value = question;
    setResultLoading(true);
    setOrbState('thinking');
    try {
      const res = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, lang: langRef.current }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok || !data) throw new Error((data && data.error) || 'HTTP ' + res.status);
      setCurrentResult(data);
      announce(data.name || data.topic || '');
    } catch (err) {
      setCurrentResult(null);
      showError(err instanceof TypeError ? t('networkError') : err.message);
    } finally {
      setBusy(false);
      setResultLoading(false);
      setOrbState('idle');
    }
  }

  /* ---------------- approach navigator ---------------- */
  useEffect(() => {
    if (view !== 'result' || !currentResult || currentResult.kind !== 'algorithm') return;
    setActiveNavId('approach-0');
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) setActiveNavId(en.target.id);
        });
      },
      { rootMargin: '-20% 0px -65% 0px' },
    );
    currentResult.approaches.forEach((_, i) => {
      const el = document.getElementById('approach-' + i);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, [currentResult, view]);

  function navigateTo(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    setActiveNavId(id);
  }

  /* ---------------- drawer ---------------- */
  function drawerAlgorithmName() {
    const r = currentResultRef.current;
    return r ? r.name || r.topic || '' : '';
  }
  function drawerApproaches() {
    const r = currentResultRef.current;
    return r && r.approaches ? r.approaches : [];
  }

  function openDrawer(focus) {
    if (!currentResultRef.current) return;
    setCurrentFocus(focus || '');
    lastFocusedRef.current = document.activeElement;
    setDrawerMounted(true);
    requestAnimationFrame(() => {
      if (drawerMountedRef.current) setDrawerOpen(true);
    });
    setTimeout(() => {
      if (drawerInputRef.current) drawerInputRef.current.focus();
    }, 280);
  }

  function closeDrawer() {
    if (!drawerOpenRef.current) return;
    setDrawerOpen(false);
    clearTimeout(drawerCloseTimerRef.current);
    drawerCloseTimerRef.current = setTimeout(() => {
      if (!drawerOpenRef.current) setDrawerMounted(false);
    }, 300);
    const lf = lastFocusedRef.current;
    if (lf && lf.focus) lf.focus();
  }

  useEffect(() => {
    const thread = threadRef.current;
    if (thread) thread.scrollTop = thread.scrollHeight;
  }, [exchanges]);

  async function sendFollowup(question) {
    question = (question || '').trim();
    if (!question || !currentResultRef.current || followupBusyRef.current) return;
    const focus = currentFocusRef.current;
    const levelText = focus
      ? t('aboutMethodChip') + ': ' + focus
      : t('aboutAlgorithmChip');
    const id = ++exchangeIdRef.current;
    setExchanges((prev) => [
      ...prev,
      { id, question, levelText, answer: t('followupWorking'), data: null },
    ]);
    if (drawerInputRef.current) drawerInputRef.current.value = '';
    setFollowupBusy(true);
    try {
      const res = await fetch('/api/followup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          lang: langRef.current,
          algorithm: drawerAlgorithmName(),
          approach: focus,
          approaches: drawerApproaches(),
        }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok || !data) throw new Error((data && data.error) || 'HTTP ' + res.status);
      setExchanges((prev) =>
        prev.map((ex) => (ex.id === id ? { ...ex, answer: data.answer || '', data } : ex)),
      );
    } catch (err) {
      setExchanges((prev) =>
        prev.map((ex) =>
          ex.id === id
            ? { ...ex, answer: err instanceof TypeError ? t('networkError') : err.message }
            : ex,
        ),
      );
    } finally {
      setFollowupBusy(false);
    }
  }

  /* ---------------- voice sheet ---------------- */
  function setVoiceState(state, data) {
    setVoiceStateBoth(state);
    if (state === 'error') setVoiceError((data && data.message) || '');
    const { title } = voiceStateText(state, t, (data && data.message) || '');
    if (title) announce(title);
  }

  function openVoice(context) {
    setVoiceContext(context || 'search');
    voiceReturnFocusRef.current = document.activeElement;
    setLastTranscript('');
    setLastAnswerText('');
    setLastAudioBase64('');
    stopAudio();
    setSheetMounted(true);
    requestAnimationFrame(() => {
      if (sheetMountedRef.current) setSheetOpen(true);
    });
    if (!keySetRef.current) {
      setVoiceState('notconfigured');
      return;
    }
    if (!recordingSupported()) {
      setVoiceState('unsupported');
      return;
    }
    setVoiceState('permission');
  }

  function closeVoiceSheet() {
    if (recorderRef.current) {
      recorderRef.current.stop();
      recorderRef.current = null;
    }
    stopAudio();
    setVoiceState('hidden');
    setSheetOpen(false);
    clearTimeout(sheetCloseTimerRef.current);
    sheetCloseTimerRef.current = setTimeout(() => {
      if (voiceStateRef.current === 'hidden') setSheetMounted(false);
    }, 280);
    setOrbState('idle');
    const rf = voiceReturnFocusRef.current;
    if (rf && rf.focus) rf.focus();
  }

  function typeInstead() {
    const wasFollowup = voiceContextRef.current === 'followup';
    closeVoiceSheet();
    setTimeout(() => {
      if (wasFollowup && drawerOpenRef.current) {
        if (drawerInputRef.current) drawerInputRef.current.focus();
      } else if (viewRef.current === 'home') {
        if (searchInputRef.current) searchInputRef.current.focus();
      } else if (resultSearchInputRef.current) {
        resultSearchInputRef.current.focus();
      }
    }, 120);
  }

  async function requestMic() {
    try {
      const recorder = new Recorder({
        onAmp: (peak) => setAmp(peak),
        onTick: (text) => {
          if (recTimerRef.current) recTimerRef.current.textContent = text;
        },
      });
      await recorder.start();
      recorderRef.current = recorder;
      setVoiceState('listening');
    } catch (e) {
      if (e && e.name === 'NotAllowedError') setVoiceState('denied');
      else setVoiceState('unsupported');
    }
  }

  async function submitVoice() {
    const recorder = recorderRef.current;
    recorderRef.current = null;
    const wav = recorder ? recorder.stop() : null;
    if (!wav) {
      setVoiceState('nospeech');
      return;
    }
    setVoiceState('processing');
    try {
      const fd = new FormData();
      fd.append('audio', wav, 'question.wav');
      fd.append('lang', langRef.current);
      if (voiceContextRef.current === 'followup' && currentResultRef.current) {
        fd.append('algorithm', drawerAlgorithmName());
        if (currentFocusRef.current) fd.append('approach', currentFocusRef.current);
        fd.append('approaches', JSON.stringify(drawerApproaches()));
      }
      const res = await fetch('/api/ask', { method: 'POST', body: fd });
      const data = await res.json().catch(() => null);
      if (!res.ok || !data) {
        if (data && data.error_code === 'NO_SPEECH') {
          setVoiceState('nospeech');
          return;
        }
        throw new Error((data && data.error) || 'HTTP ' + res.status);
      }
      const transcript = data.transcript || '';
      if (!transcript) {
        setVoiceState('nospeech');
        return;
      }
      setLastTranscript(transcript);
      const audioB64 = data.audio_base64 || '';
      setLastAudioBase64(audioB64);
      if (data.kind === 'followup') {
        const answerText = data.answer || '';
        setLastAnswerText(answerText);
        const levelText = currentFocusRef.current
          ? t('aboutMethodChip') + ': ' + currentFocusRef.current
          : t('aboutAlgorithmChip');
        const id = ++exchangeIdRef.current;
        setExchanges((prev) => [
          ...prev,
          { id, question: transcript, levelText, answer: answerText, data },
        ]);
        if (audioB64 && voiceAnswersOnRef.current) {
          playBase64Audio(audioB64, 'ex-' + id + '-listen');
          setVoiceState('speaking');
        } else {
          setVoiceState('done');
        }
      } else {
        setLastAnswerText(data.summary || data.answer || '');
        setCurrentResult(data);
        setCurrentQuestion(transcript);
        setCurrentFocus('');
        setExchanges([]);
        setView('result');
        if (audioB64 && voiceAnswersOnRef.current) {
          playBase64Audio(audioB64, null);
          setVoiceState('speaking');
        } else {
          setVoiceState('done');
        }
      }
    } catch (err) {
      setVoiceState('error', {
        message: err instanceof TypeError ? t('networkError') : err.message,
      });
    }
  }

  const voiceActions = {
    requestMic,
    submitVoice,
    closeSheet: closeVoiceSheet,
    cancelListening: () => {
      if (recorderRef.current) {
        recorderRef.current.stop();
        recorderRef.current = null;
      }
      closeVoiceSheet();
    },
    typeInstead,
    retry: () => openVoice(voiceContextRef.current),
    pausePlayer: () => {
      if (playerRef.current) playerRef.current.pause();
    },
    resumePlayer: () => {
      if (playerRef.current) playerRef.current.play();
    },
    replay: () => {
      playBase64Audio(lastAudioBase64, null);
      setVoiceState('speaking');
    },
    hasAudio: !!lastAudioBase64,
  };

  /* ---------------- settings ---------------- */
  function closeSettings() {
    setSettingsOpen(false);
  }

  useEffect(() => {
    const handler = (e) => {
      if (
        settingsOpenRef.current &&
        settingsPopoverRef.current &&
        !settingsPopoverRef.current.contains(e.target) &&
        !(settingsBtnRef.current && settingsBtnRef.current.contains(e.target))
      ) {
        closeSettings();
      }
    };
    document.addEventListener('click', handler);
    return () => document.removeEventListener('click', handler);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* ---------------- keyboard ---------------- */
  useEffect(() => {
    const handler = (e) => {
      if (e.key === 'Escape') {
        if (voiceStateRef.current !== 'hidden') {
          closeVoiceSheet();
          return;
        }
        if (drawerOpenRef.current) {
          closeDrawer();
          return;
        }
        if (settingsOpenRef.current) {
          closeSettings();
          return;
        }
      }
      if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const tag = (document.activeElement && document.activeElement.tagName) || '';
        if (
          /INPUT|TEXTAREA|SELECT/.test(tag) ||
          (document.activeElement && document.activeElement.isContentEditable)
        ) {
          return;
        }
        e.preventDefault();
        if (viewRef.current === 'home') {
          if (searchInputRef.current) searchInputRef.current.focus();
        } else if (resultSearchInputRef.current) {
          resultSearchInputRef.current.focus();
        }
      }
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* ---------------- render ---------------- */
  const orbStatusKey = ORB_STATUS_KEYS[orbState] || 'orbIdle';
  const langName = (LANG_LABELS[lang] || lang).split(' (')[0];
  const navApproaches =
    view === 'result' && !resultLoading && currentResult && currentResult.kind === 'algorithm'
      ? currentResult.approaches
      : [];

  return (
    <>
      <a className="skip-link" href="#searchInput">
        {t('skipToSearch')}
      </a>
      <div className="bg-glow" aria-hidden="true"></div>

      <header className="topbar">
        <div className="topbar-inner">
          <a
            className="wordmark"
            href="#"
            id="homeLink"
            onClick={(e) => {
              e.preventDefault();
              showHome();
            }}
          >
            <svg className="wordmark-orb" viewBox="0 0 32 32" aria-hidden="true">
              <defs>
                <radialGradient id="wmGrad" cx="35%" cy="30%" r="80%">
                  <stop offset="0%" stopColor="#B7AFFF" />
                  <stop offset="55%" stopColor="#8B7CFF" />
                  <stop offset="100%" stopColor="#5A4BD0" />
                </radialGradient>
              </defs>
              <circle cx="16" cy="16" r="14" fill="url(#wmGrad)" />
              <rect x="10" y="13" width="3" height="6" rx="1.5" fill="#fff" opacity=".9" />
              <rect x="14.5" y="10" width="3" height="12" rx="1.5" fill="#fff" />
              <rect x="19" y="13" width="3" height="6" rx="1.5" fill="#fff" opacity=".9" />
            </svg>
            <span>Bolke Seekho</span>
          </a>
          <div className="topbar-actions">
            <label className="sr-only" htmlFor="langSel">
              {t('langLabel')}
            </label>
            <select
              id="langSel"
              className="lang-select"
              aria-label="Language"
              value={lang}
              onChange={(e) => {
                setLang(e.target.value);
                store.set('bolke-lang', e.target.value);
              }}
            >
              {languages.map((l) => (
                <option key={l} value={l}>
                  {LANG_LABELS[l] || l}
                </option>
              ))}
            </select>
            <button
              type="button"
              id="settingsBtn"
              ref={settingsBtnRef}
              className="icon-btn"
              aria-haspopup="dialog"
              aria-expanded={settingsOpen ? 'true' : 'false'}
              aria-label={t('voiceSettingsAria')}
              onClick={(e) => {
                e.stopPropagation();
                setSettingsOpen(!settingsOpenRef.current);
              }}
            >
              <svg
                className="icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <line x1="4" x2="4" y1="21" y2="14" />
                <line x1="4" x2="4" y1="10" y2="3" />
                <line x1="12" x2="12" y1="21" y2="12" />
                <line x1="12" x2="12" y1="8" y2="3" />
                <line x1="20" x2="20" y1="21" y2="16" />
                <line x1="20" x2="20" y1="12" y2="3" />
                <line x1="2" x2="6" y1="14" y2="14" />
                <line x1="10" x2="14" y1="8" y2="8" />
                <line x1="18" x2="22" y1="16" y2="16" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <div
        id="settingsPopover"
        ref={settingsPopoverRef}
        className="popover"
        role="dialog"
        aria-label="Settings"
        hidden={!settingsOpen}
      >
        <div className="switch-row">
          <span id="voiceSwitchLabel">{t('voiceAnswersLabel')}</span>
          <button
            type="button"
            className="switch"
            id="voiceSwitch"
            role="switch"
            aria-checked={voiceAnswersOn ? 'true' : 'false'}
            aria-labelledby="voiceSwitchLabel"
            onClick={() => setVoiceAnswersOn(!voiceAnswersOnRef.current)}
          ></button>
        </div>
        <div className="switch-row">
          <span id="themeSwitchLabel">{t('themeLabel')}</span>
          <button
            type="button"
            className="switch"
            id="themeSwitch"
            role="switch"
            aria-checked={theme === 'light' ? 'true' : 'false'}
            aria-labelledby="themeSwitchLabel"
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
          ></button>
        </div>
        <p className="popover-note">{t('voiceSupportNote')}</p>
      </div>

      <div id="offlineBanner" className="offline-banner" role="status" hidden={online}>
        {t('offlineText')}
      </div>

      <main id="main">
        <section
          id="homeView"
          className="home"
          aria-labelledby="homeHeading"
          hidden={view !== 'home'}
        >
          <Orb prefix="home" state={orbState} id="orbWrap" className="orb-wrap" orbRef={orbWrapRef} />
          <p className="sr-only" role="status" id="orbStatus">
            {t(orbStatusKey)}
          </p>
          <h1 id="homeHeading">{t('reviseHeading')}</h1>
          <p className="home-sub">{t('homeSub')}</p>

          <SearchBox
            inputId="searchInput"
            suggestBoxId="suggestBox"
            micBtnId="micBtn"
            formId="searchForm"
            t={t}
            onSearch={runSearch}
            onMic={() => openVoice('search')}
            inputRef={searchInputRef}
          />

          <div className="chips" id="exampleChips" aria-label="Example questions">
            {['prime number', 'quicksort', 'BFS', 'two sum'].map((q) => (
              <button
                key={q}
                type="button"
                className="chip"
                data-q={q}
                onClick={() => {
                  if (searchInputRef.current) searchInputRef.current.value = q;
                  runSearch(q);
                }}
              >
                <svg
                  className="icon-sm"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M7 7h10v10" />
                  <path d="M7 17 17 7" />
                </svg>
                {q}
              </button>
            ))}
          </div>

          <p className="quiet">{t('supportingText')}</p>
          <p className="voice-note" id="voiceNote" hidden={keySet}>
            {t('noKeyBanner')}
          </p>
        </section>

        <section
          id="resultView"
          className="result-view"
          hidden={view !== 'result'}
          aria-labelledby="resultHeading"
        >
          <h2 id="resultHeading" className="sr-only">
            {t('resultHeading')}
          </h2>
          <div className="result-topbar">
            <button
              type="button"
              id="backBtn"
              className="btn btn-ghost"
              onClick={() => {
                showHome();
                if (searchInputRef.current) searchInputRef.current.focus();
              }}
            >
              <svg
                className="icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="m12 19-7-7 7-7" />
                <path d="M19 12H5" />
              </svg>
              <span>{t('newSearchButton')}</span>
            </button>
            <SearchBox
              inputId="resultSearchInput"
              suggestBoxId="resultSuggestBox"
              micBtnId="resultMicBtn"
              formId="resultSearchForm"
              compact
              t={t}
              onSearch={runSearch}
              onMic={() => openVoice('search')}
              inputRef={resultSearchInputRef}
            />
            <div id="errorBox" className="error-box" role="alert" hidden={!error}>
              {error && (
                <>
                  <Icon name="alert" />
                  <div>
                    <strong>{t('errorTitle')}</strong> {error}
                  </div>
                </>
              )}
            </div>
          </div>
          <div className="result-grid">
            <ResultView
              data={currentResult}
              loading={resultLoading}
              t={t}
              keySet={keySet}
              isDesktop={isDesktop}
              playBtn={playBtn}
              playerState={playerState}
              speakBusyId={speakBusyId}
              onToggleSpeak={toggleSpeak}
              onOpenDrawer={openDrawer}
              onAskMethod={(name) => openDrawer(name)}
              onSuggestSearch={runSearch}
            />
            <ApproachNav
              approaches={navApproaches}
              activeId={activeNavId}
              t={t}
              onNavigate={navigateTo}
            />
          </div>
        </section>
      </main>

      <footer className="page-footer">
        <p>{t('footerNote')}</p>
      </footer>

      <Drawer
        mounted={drawerMounted}
        open={drawerOpen}
        algorithmName={drawerAlgorithmName()}
        focus={currentFocus}
        approaches={drawerApproaches()}
        exchanges={exchanges}
        t={t}
        keySet={keySet}
        playBtn={playBtn}
        playerState={playerState}
        speakBusyId={speakBusyId}
        onClose={closeDrawer}
        onSendFollowup={sendFollowup}
        onMic={() => openVoice('followup')}
        onToggleSpeak={toggleSpeak}
        inputRef={drawerInputRef}
        threadRef={threadRef}
      />

      <VoiceSheet
        mounted={sheetMounted}
        open={sheetOpen}
        voiceState={voiceState}
        errorMessage={voiceError}
        transcript={lastTranscript}
        answerText={lastAnswerText}
        answerLangSpoken={!!(LANG_META[lang] && LANG_META[lang].spoken)}
        langName={langName}
        orbState={orbState}
        t={t}
        recTimerRef={recTimerRef}
        ampMeterRef={ampMeterRef}
        voiceOrbRef={voiceOrbRef}
        actions={voiceActions}
      />

      <div id="livePolite" ref={livePoliteRef} className="sr-only" aria-live="polite"></div>
      <div
        id="liveAssertive"
        ref={liveAssertiveRef}
        className="sr-only"
        aria-live="assertive"
      ></div>
      <audio
        id="player"
        ref={playerRef}
        preload="none"
        onPlaying={handlePlaying}
        onPause={handlePause}
        onEnded={handleEnded}
      ></audio>
    </>
  );
}
