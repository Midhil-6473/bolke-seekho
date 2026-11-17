import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import { Icon } from '../icons.jsx';

// Search box with live suggestions — port of bindSuggest() in the
// original page, including the sequence guard that stops a stale
// suggestions dropdown reappearing over a result after a search.
const SearchBox = forwardRef(function SearchBox(
  { inputId, suggestBoxId, micBtnId, formId, compact, t, onSearch, onMic, inputRef },
  ref,
) {
  const [items, setItems] = useState([]);
  const [active, setActive] = useState(-1);
  const [visible, setVisible] = useState(false);
  const timerRef = useRef(null);
  const blurTimerRef = useRef(null);
  const seqRef = useRef(0);

  const hide = () => {
    seqRef.current += 1;
    setVisible(false);
    setActive(-1);
  };

  useImperativeHandle(ref, () => ({ hide }));

  useEffect(
    () => () => {
      clearTimeout(timerRef.current);
      clearTimeout(blurTimerRef.current);
    },
    [],
  );

  const submitWith = (value) => {
    hide();
    onSearch(value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitWith(inputRef.current ? inputRef.current.value : '');
  };

  const fetchSugg = async (q) => {
    const s = seqRef.current;
    try {
      const res = await fetch('/api/suggest?q=' + encodeURIComponent(q) + '&limit=6');
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      if (s !== seqRef.current || (inputRef.current && inputRef.current.value.trim() !== q)) return;
      const list = data.suggestions || [];
      setItems(list);
      setActive(-1);
      setVisible(list.length > 0);
    } catch (e) {
      hide();
    }
  };

  const handleInput = () => {
    clearTimeout(timerRef.current);
    const q = inputRef.current ? inputRef.current.value.trim() : '';
    if (q.length < 2) {
      hide();
      return;
    }
    timerRef.current = setTimeout(() => fetchSugg(q), 180);
  };

  const handleKeyDown = (e) => {
    if (!visible) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      setActive((prev) =>
        e.key === 'ArrowDown' ? Math.min(prev + 1, items.length - 1) : Math.max(prev - 1, 0),
      );
    } else if (e.key === 'Enter' && active >= 0 && items[active]) {
      e.preventDefault();
      if (inputRef.current) inputRef.current.value = items[active].name;
      submitWith(items[active].name);
    } else if (e.key === 'Escape') {
      hide();
    }
  };

  const handleBoxMouseDown = (e) => {
    const btn = e.target.closest('.suggest-item');
    if (!btn) return;
    e.preventDefault();
    const name = btn.dataset.name;
    if (inputRef.current) inputRef.current.value = name;
    submitWith(name);
  };

  const handleBlur = () => {
    blurTimerRef.current = setTimeout(hide, 150);
  };

  return (
    <form
      id={formId}
      className={compact ? 'search-box search-box-compact' : 'search-box'}
      role="search"
      autoComplete="off"
      onSubmit={handleSubmit}
    >
      <Icon name="search" className="icon search-icon" />
      <label className="sr-only" htmlFor={inputId}>
        {t('searchAriaLabel')}
      </label>
      <input
        ref={inputRef}
        id={inputId}
        type="text"
        enterKeyHint="search"
        placeholder={t('searchPlaceholder')}
        aria-describedby={compact ? undefined : 'searchHintText'}
        aria-controls={suggestBoxId}
        aria-expanded={visible ? 'true' : 'false'}
        aria-activedescendant={active >= 0 ? `${suggestBoxId}-${active}` : undefined}
        role="combobox"
        aria-autocomplete="list"
        onInput={handleInput}
        onKeyDown={handleKeyDown}
        onBlur={handleBlur}
      />
      {!compact && (
        <kbd id="slashHint" aria-hidden="true">
          /
        </kbd>
      )}
      <button
        type="button"
        id={micBtnId}
        className="mic-btn"
        aria-label={t('micStart')}
        onClick={onMic}
      >
        <Icon name="mic" />
      </button>
      {!compact && (
        <span id="searchHintText" className="sr-only">
          {t('searchHint')}
        </span>
      )}
      <div
        id={suggestBoxId}
        className="suggest-box"
        role="listbox"
        hidden={!visible}
        onMouseDown={handleBoxMouseDown}
      >
        {items.map((s, i) => (
          <button
            key={s.name}
            type="button"
            className={'suggest-item' + (i === active ? ' active' : '')}
            role="option"
            id={`${suggestBoxId}-${i}`}
            data-name={s.name}
          >
            <span>{s.name}</span>
            <small>{s.category}</small>
          </button>
        ))}
      </div>
    </form>
  );
});

export default SearchBox;
