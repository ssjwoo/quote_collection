export const Search = () => {
  return (
    <div className="bg-main-beige p-8 pt-14 w-4/5 mt-14 rounded-xl shadow-xl flex flex-nowrap">
      <input
        type="text"
        placeholder="검색어를 입력하세요"
        className="w-3/4 p-2 h-7 border-b-1 opacity-80  focus:outline-none placeholder:text-sm text-center"
      />
      <button className="bg-main-white p-2 ml-3 rounded-md">search</button>
    </div>
  );
};
