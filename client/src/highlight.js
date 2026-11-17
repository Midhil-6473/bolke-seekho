// HTML escaping + lightweight Java syntax highlighting.
// Copied verbatim in behaviour from templates/index.html.

export const esc = (s) =>
  String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

const JAVA_KW =
  'abstract|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|native|new|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volatile|while|true|false|null|var';

export function highlight(code) {
  const e = esc(code);
  const re = new RegExp(
    '(\\/\\/[^\\n]*)|("(?:[^"\\\\\\n]|\\\\.)*")|\\b(' +
      JAVA_KW +
      ')\\b|\\b(\\d[\\d_]*\\.?\\d*)\\b|([A-Za-z_][\\w]*)(?=\\s*\\()',
    'g',
  );
  return e.replace(re, (m, com, str, kw, num) => {
    if (com) return '<span class="tok-com">' + m + '</span>';
    if (str) return '<span class="tok-str">' + m + '</span>';
    if (kw) return '<span class="tok-kw">' + m + '</span>';
    if (num) return '<span class="tok-num">' + m + '</span>';
    return '<span class="tok-fn">' + m + '</span>';
  });
}
