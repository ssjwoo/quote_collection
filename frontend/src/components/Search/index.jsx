import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
export const Search = ({prevInput}) => {

  const navigation = useNavigate();
  const [input,setInput]=useState(prevInput||'');

  const handleKeyDown =(e)=>{
    if(e.key === 'Enter')
      onSearchList();
  }

  const onSearchList =()=>{
    if(!input.trim()){
      alert('검색어를 입력해주세요');
      return;
    }
    navigation('/searchlist/'+input);
  }

  return (
    <div className="bg-main-beige p-8 pt-14 w-4/5 mt-14 rounded-xl shadow-xl flex justify-center flex-nowrap border border-main-green">
      <input
        type="text"
        placeholder="검색어를 입력하세요"
        value={input}
        onChange={(e)=>setInput(e.target.value)}
        onKeyDown={handleKeyDown} 
        className="w-3/4 p-2 h-7 border-b-1 opacity-80  focus:outline-none placeholder:text-sm text-center"
      />
      <button className="bg-main-white p-2 ml-3 rounded-md cursor-pointer"onClick={onSearchList}>search</button>
    </div>
  );
};
