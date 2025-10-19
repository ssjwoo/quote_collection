import { useEffect, useState } from "react";
import { Search } from "../../components/Search";
import { useNavigate, useParams } from "react-router-dom";

export const SearchList =()=>{

    const navigation = useNavigate();
    const {input} = useParams();
    /** 검색어가 포함된 db 결과 조회 (quotes, book, drama, movie) */
    const [result, setResult]=useState([]);

    useEffect(()=>{
        /**dummy */
        setResult([{id:0,title:'little princess',content:'once upon a time~'},
                    {id:32,title:'princess and the frog',content:'almot there'}
        ])
    },[input]);

     const onDetail=(id)=>{
        navigation('/detail/'+id);
    }

    return(
        <>
        <div className="flex justify-center">
        <Search prevInput={input}/>
        </div>
         <div className="text-main-green flex mt-10 justify-center">
            " {input} " results
        </div>
        <div className="flex flex-col justify-items-center mt-7">
            {result.map((r)=>(
        <div key={r.id} className=" cursor-pointer mt-5 border-2 hover:bg-main-beige border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg" onClick={() => onDetail(r.id)}> 
            <div className=" pl-3 pb-3 text-sm text-start">{r.title} </div>
            <div className="text-lg">{r.content}</div>
          </div>
        ))}
        </div>
        </>        
    );
}