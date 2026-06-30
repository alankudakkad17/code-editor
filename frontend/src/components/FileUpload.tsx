import { useRef } from "react";

interface Props {
  fileName: string | null;
  onFileSelect: (name: string, content: string) => void;
  onClear: () => void;
}

export function FileUpload({ fileName, onFileSelect, onClear }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const content = await file.text();
    onFileSelect(file.name, content);
    e.target.value = "";
  };

  if (fileName) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-700 rounded-lg text-sm text-gray-200">
        <span>📎 {fileName}</span>
        <button onClick={onClear} className="text-gray-400 hover:text-white">
          ✕
        </button>
      </div>
    );
  }

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept=".py,.js,.ts,.tsx,.jsx,.txt"
        className="hidden"
        onChange={handleChange}
      />
      <button
        onClick={() => inputRef.current?.click()}
        className="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm text-gray-300 transition-colors"
        title="Upload a file"
      >
        📁 Attach
      </button>
    </>
  );
}
