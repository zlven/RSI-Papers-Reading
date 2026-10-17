// MathJax 3 配置 —— 配合 mkdocs.yml 中的 pymdownx.arithmatex (generic: true)。
// generic 模式只把 \(...\) 与 \[...\] 交给 MathJax，$...$ 保持普通文本，
// 避免把 $5000 这类货币金额误渲染成公式。
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    // 只处理 arithmatex 生成的节点，其余 HTML（尤其货币金额）一律跳过
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// navigation.instant 是站内无刷新跳转：每次切换页面后需重新排版公式。
document$.subscribe(() => {
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
