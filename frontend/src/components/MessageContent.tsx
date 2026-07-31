import { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

function CodeBlock({ language, code }: { language: string; code: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="relative my-2 rounded-lg overflow-hidden border border-gray-700">
      <div className="flex items-center justify-between px-3 py-1.5 bg-gray-800 text-xs text-gray-400">
        <span className="uppercase tracking-wide">{language || "text"}</span>
        <button
          onClick={handleCopy}
          className="px-2 py-0.5 rounded hover:bg-gray-700 transition-colors text-xs"
        >
          {copied ? "✓ Copied" : "📋 Copy"}
        </button>
      </div>
      <SyntaxHighlighter
        language={language || "text"}
        style={vscDarkPlus}
        customStyle={{ margin: 0, fontSize: "13px", padding: "12px" }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}

export function MessageContent({ text }: { text: string }) {
  const parts = text.split(/(```[\w]*\n[\s\S]*?```)/g);

  return (
    <div className="space-y-1">
      {parts.map((part, i) => {
        const match = part.match(/```(\w+)?\n([\s\S]*?)```/);
        if (match) {
          const [, lang, code] = match;
          return <CodeBlock key={i} language={lang || "text"} code={code.trimEnd()} />;
        }
        if (!part.trim()) return null;
        return (
          <p key={i} className="whitespace-pre-wrap leading-relaxed">
            {part}
          </p>
        );
      })}
    </div>
  );
}
