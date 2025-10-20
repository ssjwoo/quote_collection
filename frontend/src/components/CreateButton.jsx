export default function CreateButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="text-left px-2 py-1 rounded border border-dashed text-custom-basic-font border-white text-gray-600 hover:bg-gray-100 bg-white/30"
    >
      +
    </button>
  );
}
