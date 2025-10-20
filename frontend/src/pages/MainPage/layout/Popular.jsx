import { useNavigate } from "react-router-dom";

export const Popular =({popularQuote})=>{

    const navigation = useNavigate();
    
    const onDetail=(id)=>{
        navigation('/detail/'+id);
    }

    return(
        <>
        <div className="flex-col flex items-center">
          <div className="mt-9 mb-4 text-3xl">POPULAR</div>
          <div className=" cursor-pointer h-56 bg-sub-darkbeidge rounded-xl shadow-xl w-4/5 " onClick={()=>onDetail(popularQuote.id)}>
            <div className=" h-1/6 flex justify-start p-3">{popularQuote.title}</div>
            <div className="h-4/6 flex justify-center p-3">{popularQuote.content}</div>
            <div className="h-1/6 flex justify-end pb-3 pr-3">{popularQuote.creater}</div>
          </div>
        </div>
        </>
    );
}