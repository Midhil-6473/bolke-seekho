import { useEffect, useRef } from 'react';
import { Icon } from '../icons.jsx';
import { Orb } from '../orb.jsx';

// Voice sheet state machine — port of setVoiceState() in the original
// page. All 10 voice states plus the error state, with transcript and
// answer boxes and a text fallback on every failure state.

export function voiceStateText(state, t, errorMessage) {
  switch (state) {
    case 'permission':
      return { title: t('sheetPermissionTitle'), desc: t('sheetPermissionText') };
    case 'listening':
      return { title: t('sheetListeningTitle'), desc: t('sheetListeningText') };
    case 'processing':
      return { title: t('sheetProcessingTitle'), desc: t('sheetProcessingText') };
    case 'speaking':
      return { title: t('sheetSpeakingTitle'), desc: t('sheetSpeakingText') };
    case 'paused':
      return { title: t('sheetPausedTitle'), desc: t('sheetPausedText') };
    case 'done':
      return { title: t('sheetDoneTitle'), desc: t('sheetDoneText') };
    case 'nospeech':
      return { title: t('sheetNoSpeechTitle'), desc: t('sheetNoSpeechText') };
    case 'denied':
      return { title: t('sheetDeniedTitle'), desc: t('sheetDeniedText') };
    case 'notconfigured':
      return { title: t('sheetNotConfiguredTitle'), desc: t('sheetNotConfiguredText') };
    case 'unsupported':
      return { title: t('sheetUnsupportedTitle'), desc: t('sheetUnsupportedText') };
    case 'error':
      return { title: t('errorTitle'), desc: errorMessage || t('networkError') };
    default:
      return { title: '', desc: '' };
  }
}

function voiceControlsFor(state, t, a) {
  switch (state) {
    case 'permission':
      return [
        { label: t('allowMicButton'), kind: 'btn-primary', iconName: 'mic', onClick: a.requestMic },
        { label: t('cancelButton'), kind: 'btn-ghost', onClick: a.closeSheet },
      ];
    case 'listening':
      return [
        { label: t('stopButton'), kind: 'btn-danger', iconName: 'stop', onClick: a.submitVoice },
        { label: t('cancelButton'), kind: 'btn-ghost', onClick: a.cancelListening },
      ];
    case 'processing':
      return [];
    case 'speaking':
      return [
        { label: t('pauseButton'), kind: 'btn-secondary', iconName: 'pause', onClick: a.pausePlayer },
        { label: t('closeButton'), kind: 'btn-ghost', onClick: a.closeSheet },
      ];
    case 'paused':
      return [
        { label: t('resumeButton'), kind: 'btn-primary', iconName: 'play', onClick: a.resumePlayer },
        { label: t('closeButton'), kind: 'btn-ghost', onClick: a.closeSheet },
      ];
    case 'done': {
      const defs = [];
      if (a.hasAudio) {
        defs.push({
          label: t('replayButton'),
          kind: 'btn-secondary',
          iconName: 'play',
          onClick: a.replay,
        });
      }
      defs.push(
        { label: t('retryButton'), kind: 'btn-secondary', iconName: 'retry', onClick: a.retry },
        { label: t('closeButton'), kind: 'btn-ghost', onClick: a.closeSheet },
      );
      return defs;
    }
    case 'nospeech':
      return [
        { label: t('retryButton'), kind: 'btn-primary', iconName: 'retry', onClick: a.retry },
        { label: t('useTextButton'), kind: 'btn-secondary', onClick: a.typeInstead },
        { label: t('closeButton'), kind: 'btn-ghost', onClick: a.closeSheet },
      ];
    case 'denied':
    case 'notconfigured':
    case 'unsupported':
      return [
        { label: t('useTextButton'), kind: 'btn-primary', onClick: a.typeInstead },
        { label: t('closeButton'), kind: 'btn-ghost', onClick: a.closeSheet },
      ];
    case 'error':
      return [
        { label: t('retryButton'), kind: 'btn-primary', iconName: 'retry', onClick: a.retry },
        { label: t('closeButton'), kind: 'btn-ghost', onClick: a.closeSheet },
      ];
    default:
      return [];
  }
}

export default function VoiceSheet({
  mounted,
  open,
  voiceState,
  errorMessage,
  transcript,
  answerText,
  answerLangSpoken,
  langName,
  orbState,
  t,
  recTimerRef,
  ampMeterRef,
  voiceOrbRef,
  actions,
}) {
  const controlsRef = useRef(null);

  // The original focuses the first control button every time the
  // state's controls are (re)built.
  useEffect(() => {
    if (!open) return;
    const first = controlsRef.current && controlsRef.current.querySelector('button');
    if (first) first.focus();
  }, [voiceState, open]);

  if (!mounted) return null;

  const { title, desc } = voiceStateText(voiceState, t, errorMessage);
  const showTranscript =
    (voiceState === 'processing' ||
      voiceState === 'speaking' ||
      voiceState === 'paused' ||
      voiceState === 'done') &&
    !!transcript;
  const showAnswer =
    (voiceState === 'speaking' || voiceState === 'paused' || voiceState === 'done') &&
    !!answerText;
  const controls = voiceControlsFor(voiceState, t, actions);

  return (
    <div
      id="voiceSheet"
      className={'voice-sheet' + (open ? ' open' : '')}
      role="dialog"
      aria-modal="true"
      aria-labelledby="voiceStateTitle"
    >
      <button
        type="button"
        id="voiceSheetClose"
        className="icon-btn voice-close"
        aria-label={t('closeButton')}
        onClick={actions.closeSheet}
      >
        <Icon name="x" />
      </button>
      <Orb prefix="sheet" state={orbState} id="voiceOrb" className="orb-wrap orb-mini" orbRef={voiceOrbRef} />
      <h2 id="voiceStateTitle">{title}</h2>
      <p className="voice-desc" id="voiceStateDesc">
        {desc}
      </p>
      <p className="rec-timer" id="recTimer" ref={recTimerRef} hidden={voiceState !== 'listening'}>
        0:00
      </p>
      <div
        className="amp-meter"
        id="ampMeter"
        ref={ampMeterRef}
        hidden={voiceState !== 'listening'}
        aria-hidden="true"
      >
        <i></i>
      </div>
      <div id="voiceTranscript" className="voice-transcript" hidden={!showTranscript}>
        <p className="box-label">
          <span>{t('transcriptLabel')}</span> · <span>{t('heardInLabel')}</span>{' '}
          <span id="voiceLangName">{langName}</span>
        </p>
        <p id="voiceTranscriptText">{transcript}</p>
      </div>
      <div id="voiceAnswerBox" className="voice-answer-box" hidden={!showAnswer}>
        <p className="box-label">{t('voiceAnswerLabel')}</p>
        <p id="voiceAnswerText">
          {answerText}
          {!answerLangSpoken && (
            <>
              <br />
              <span style={{ color: 'var(--text-2)', fontSize: '13.5px' }}>
                {t('englishFallbackNote')}
              </span>
            </>
          )}
        </p>
      </div>
      <div className="voice-controls" id="voiceControls" ref={controlsRef}>
        {controls.map((d) => (
          <button
            key={d.label}
            type="button"
            className={'btn ' + (d.kind || 'btn-secondary')}
            onClick={d.onClick}
          >
            {d.iconName && <Icon name={d.iconName} className="icon-sm" />}
            <span>{d.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
