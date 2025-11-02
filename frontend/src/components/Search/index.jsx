import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import search from "../../assets/search.png"

export const Search = ({prevInput, source_type}) => {

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
    let path = '/searchlist/'+input;
    if (source_type) {
      path += `?source_type=${source_type}`;
    }
    navigation(path);
  }

  return (
    <div className="bg-main-beige/50 p-8 pt-14 w-4/5 mt-14 rounded-xl shadow-xl flex justify-center flex-nowrap border-2 border-main-green">
      <input
        type="text"
        placeholder="검색어를 입력하세요"
        value={input}
        onChange={(e)=>setInput(e.target.value)}
        onKeyDown={handleKeyDown} 
        className="w-3/4 p-2 h-7 border-b-1 mt-4 opacity-80 focus:outline-none placeholder:text-sm text-center"
      />
      <button className=" text-white p-2 ml-3 rounded-md cursor-pointer"onClick={onSearchList}><img className="w-10"  src={search}/></button>
    </div>
  );
};
