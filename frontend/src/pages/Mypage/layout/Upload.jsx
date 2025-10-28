import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const Upload =()=>{

    const navigation = useNavigate();
    const [quotes,setQuotes]=useState([]);
    
        useEffect(()=>{
            // TODO: API call here
            /**사용자가 upload 한 quote 모두 불러오기 */
            /**dummy */
            setQuotes([{id:0,title:'little princess',content:'once upon a time~',creater:'b111',createdAt:'2000-10-22'},
                        {id:32,title:'princess and the frog',content:'almot there',creater:'abab',createdAt:'2025-10-11'}
            ])
        },[]);
    
         const onDetail=(id)=>{
            navigation('/detail/'+id);
        }

    return(
        <>
        <div className="flex flex-col justify-items-center m-3">
            {quotes.map((q)=>(
        <div key={q.id} className=" cursor-pointer mt-5 border-2 hover:bg-main-beige border-main-green h-full pt-5 pb-5 text-center rounded-lg shadow-lg" 
        onClick={() => onDetail(q.id)}> 
            <div className=" pl-3 pb-3 text-sm text-start">{q.title} </div>
            <div className="text-lg">{q.content}</div>
            <div className="text-xs text-end pr-3"><span className="mr-2 font-bold">{q.creater}</span>{q.createdAt}</div>
          </div>
        ))}
        </div>
        </>
    );
}