import { useEffect, useRef, useState } from 'react';
import { Icon } from '../icons.jsx';
import { copyText } from '../clipboard.js';
import { highlight } from '../highlight.js';

// Copy button with the original's 1600 ms "Copied" feedback.
export function CopyButton({ text, label, copiedLabel, className }) {
  const [copied, setCopied] = useState(false);
  const timerRef = useRef(null);
  useEffect(() => () => clearTimeout(timerRef.current), []);
  const handleClick = async () => {
    await copyText(text);
    setCopied(true);
    clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => setCopied(false), 1600);
  };
  return (
    <button type="button" className={className || 'copy-btn'} onClick={handleClick}>
      {copied ? (
        <>
          <Icon name="check" className="icon-sm" />
          <span>{copiedLabel}</span>
        </>
      ) : (
        <>
          <Icon name="copy" className="icon-sm" />
          <span>{label}</span>
        </>
      )}
    </button>
  );
}

// Listen button: its label tracks the shared player (Listen / Pause /
// Resume) when it is the button that started the current playback.
export function ListenButton({
  id,
  text,
  t,
  playBtn,
  playerState,
  disabled,
  onToggle,
  className,
}) {
  const isActive = playBtn === id;
  const playing = isActive && playerState === 'playing';
  const paused = isActive && playerState === 'paused';
  return (
    <button
      type="button"
      className={className || 'btn btn-voice'}
      aria-pressed={playing ? 'true' : 'false'}
      disabled={disabled}
      onClick={() => onToggle(text, id)}
    >
      {playing ? (
        <>
          <Icon name="pause" className="icon-sm" />
          <span>{t('pauseButton')}</span>
        </>
      ) : paused ? (
        <>
          <Icon name="play" className="icon-sm" />
          <span>{t('resumeButton')}</span>
        </>
      ) : (
        <>
          <Icon name="volume" className="icon-sm" />
          <span>{t('listenButton')}</span>
        </>
      )}
    </button>
  );
}

export function CodePanel({ title, code, copyLabel, copiedLabel }) {
  return (
    <div className="code-panel">
      <div className="code-panel-head">
        <span className="approach-name">{title}</span>
        <span className="spacer"></span>
        <CopyButton text={code} label={copyLabel} copiedLabel={copiedLabel} />
      </div>
      <pre>
        <code dangerouslySetInnerHTML={{ __html: highlight(code) }} />
      </pre>
    </div>
  );
}

export function ComplexityChip({ label, value }) {
  return (
    <span className="complexity">
      {label} <b>{value}</b>
    </span>
  );
}
