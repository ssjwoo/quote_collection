import { useNavigate } from "react-router-dom";

export const Popular = ({ mode, popularQuote }) => {
  const navigation = useNavigate();
  // console.log(popularQuote);
  //TODO:popular quote 에 id가 없어서 detail page로 넘어가는 것이 불가
   const onDetail=(id)=>{
        navigation('/quote/'+id, {
    state: {
      mode: mode
    }})
    }

  return (
    <>
      <div className="flex-col flex items-center">
        <div className="mt-9 mb-4 text-3xl">POPULAR</div>
        {popularQuote && popularQuote.title ? (
          <div
            className=" cursor-pointer h-56 bg-sub-darkbeidge rounded-xl shadow-xl w-4/5 "
            onClick={() => onDetail(popularQuote.id)}
          >
            <div className=" h-1/6 flex justify-start p-3">
              {popularQuote.title}
            </div>
            <div className="h-4/6 flex justify-center p-3">
              {popularQuote.content}
            </div>
            <div className="h-1/6 flex justify-end pb-3 pr-3">
              {popularQuote.creator}
            </div>
          </div>
        ) : (
          <div className="h-56 flex justify-center items-center bg-sub-darkbeidge rounded-xl shadow-xl w-4/5 ">
            <p>Loading popular quote...</p>
          </div>
        )}
      </div>
    </>
  );
};
