import { useNavigate } from 'react-router-dom';
import mark from '../../../assets/bookmark.png';
import marked from '../../../assets/bookmark_marked.png';
import { useEffect, useState } from 'react';

export const MovieDetail =({quote})=>{

 const navigation = useNavigate();
 const [isLogin, setIsLogin] = useState(true);
 const [bookmark, setBookMarked] = useState(true);
 const [user,setUser] = useState({});

 useEffect(()=>{
    if(isLogin){
        /**dummy */
        setUser({id:'user1',bookmark:{'book':[1,2,3], 'funny':[1,2]}})
        /** 사용자 정보의 bookmark에 이 글이 있는지 확인*/
        setBookMarked(true);
    }
    
 },[isLogin]);

 const onIsLogin =()=>{
    if(!isLogin){
        alert('로그인이 필요한 기능입니다.');
        return;
    }
    /** DB 사용자 북마크 데이터 업데이트 필요 */
    setBookMarked(!bookmark);
 }

  const onSearchList =(input)=>{
    navigation('/searchlist/'+input);
  }
   const onModify =()=>{
    navigation('/detail/'+quote.id+'/modi');
  }
  const onDelete=()=>{
    
  }

    return(
        <>
         <div className="flex flex-col mt-10">
                  <div className="text-3xl mb-5">MOVIE MOMENT</div>
                   {/* 글 작성자에게만 보이도록 */}
                  {(user.id == quote.writer) &&
                    <div className='text-end'> 
                        <button className='px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs mr-2' onClick={onModify}>수정</button> 
                        <button className='px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs' onClick={onDelete}>삭제 </button>
                    </div>}
                       <div className="flex items-end mt-3">
                        <label className="w-1/12 text-sm text-end pb-3">영화 제목 </label>
                        <div className="w-4/6 text-start text-xl rounded-lg p-2 pl-4 ml-3">
                            <span className='cursor-pointer' onClick={()=>onSearchList(quote.title)}>{quote.title}</span></div>
                    </div>
                     <div className="flex justify-center mt-3">  
                        <div className="w-4/5 text-main-white pt-12 pb-12 bg-main-green rounded-lg p-2 pl-4 ml-3 shadow-lg shadow-gray-400">{quote.content}</div>
                     </div>
                    <div className="flex justify-end mt-3">  
                        <div className=" flex border-2 border-sub-darkgreen w-1/12 items-end rounded-lg p-3 mr-14">
                            <img className="size-5 cursor-pointer" onClick={onIsLogin} src={(isLogin&&bookmark)?marked:mark}/>
                        </div>
                     </div>
                     <div className="flex items-end mt-3">
                        <label className="w-1/12 text-end pb-3 text-sm">감독 </label>
                        <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3" >
                            <span className='cursor-pointer' onClick={()=>onSearchList(quote.creater)}>{quote.creater}</span></div>
                    </div>
        
                    {quote.subData && (<>
                    <div className="flex items-end mt-3">
                        <label className="w-1/12 text-end pb-3 text-sm">개봉일 </label>
                        <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">{quote.subData}</div>
                        </div></>)} 
        
                    {quote.tags && (
                    <div className="flex items-end mt-3">
                         <label className="w-1/12 text-end pb-3 text-sm">TAGS </label>
                        <div className="w-4/6 text-start rounded-lg p-2 pl-4 ">
                        {quote.tags.map(
                            (t)=>(
                                <span key={t.id} onClick={()=>onSearchList(t)} className="rounded-xl p-2 cursor-pointer bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border">{t}</span>
                            )
                        )}</div>
                    </div>
                    )}
                    
                </div>
        
        </>
    );
}