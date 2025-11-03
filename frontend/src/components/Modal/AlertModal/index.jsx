
export const AlertModal = ({ open, onClose, message }) => {
  if (!open) return null;

  return (
    <div className="fixed inset-0 flex bg-black/40 justify-center items-center z-50">
      <div className="bg-white/80 rounded-2xl shadow-lg p-6 w-72 text-center">
        <p className="text-gray-700 mb-5 text-sm">{message}</p>
        <button
          onClick={onClose}
          className="bg-main-green hover:bg-mypage-menu text-xs hover:text-main-green text-white px-5 py-2 mt-3 rounded-xl transition"
        >
          확인
        </button>
      </div>
    </div>
  );
};
