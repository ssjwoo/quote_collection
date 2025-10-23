// src/components/Modal/NameModal.jsx
import { useState } from "react";

export default function NameModal({ open, onClose, onConfirm }) {
  const [value, setValue] = useState("");
  if (!open) return null;

  const confirm = () => {
    const name = value.trim();
    if (!name) return;
    onConfirm(name);
    setValue("");
  };

  return (
    <div
      className="fixed inset-0 z-[9999] flex justify-center items-center bg-black/50"
      onClick={onClose}
    >
      <div onClick={(e) => e.stopPropagation()} className="relative">
        <div className="z-50 bg-main-green/80 h-[200px] w-[400px] rounded-sm flex flex-col items-start md:items-center justify-between md:justify-center p-4">
          <div className="text-custom-div text-3xl mb-5 cursor-default">
            FOLDER
          </div>

          <form
            className="w-full flex flex-col items-stretch space-y-3"
            onSubmit={(e) => {
              e.preventDefault();
              confirm();
            }}
          >
            <input
              autoFocus
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && confirm()}
              placeholder="폴더 이름을 입력하세요"
              className="w-full bg-white rounded-md shadow-md focus:shadow-lg focus:outline-none p-2"
            />

            <div className="flex items-center justify-end gap-2">
              <button
                type="button"
                onClick={() => {
                  setValue("");
                  onClose();
                }}
                className="border border-custom-div text-custom-div w-[70px] h-[30px] rounded-sm flex justify-center items-center hover:bg-custom-div hover:text-main-green transition"
              >
                cancel
              </button>
              <button
                type="submit"
                className="bg-custom-div w-[70px] h-[30px] rounded-sm flex justify-center items-center"
              >
                confirm
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
