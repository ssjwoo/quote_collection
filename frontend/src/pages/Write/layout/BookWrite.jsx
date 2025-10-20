import { useEffect, useState } from "react";
import { Form } from "react-router-dom";

export const BookWrite = () =>{
    
    const[user,setUser] = useState({id:'1',email:'111@naber.com',name:'user1'});
    const[title, setTitle] = useState('');
    const[author, setAuthor] = useState('');
    const[publisher, setPublisher] = useState('');
    const[content, setContent] = useState('');

    const tags = ['사랑','이별','그리움','설렘','추억','희망','용기','성장','변화','새로움','고독','불안','혼란','상처','치유','평온','잔잔함','빛','어둠','자유','꿈','여행','일상','철학'];
    const [selectedTags,setSelectedTags]=useState([]);
    const [error, setError]=useState('');
    const [charNum,setCharNum]=useState(0);
    
    /** tag 선택, 미선택 스타일 변경 */
    const style = ["rounded-xl p-2 bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border",
        "rounded-xl p-2 bg-main-pink text-xs ml-1 mr-1 mb-1 border-main-green border"]

    useEffect(()=>{
        if(selectedTags.length <5)
            setError('')
    },[selectedTags]);

    const onSelected=(id)=>{
        setSelectedTags((prevSelected)=>{
            if (prevSelected.includes(id)) {
                return prevSelected.filter((tid) => tid !== id);
            }else{
                if(selectedTags.length==5){
                    setError('태그 선택은 최대 5개까지만 가능합니다.');
                    return[...prevSelected];                
                }
                return [...prevSelected, id];
            }
        })
    }

    const onSubmit=()=>{
        if(!title.trim()||!author.trim()||!content.trim()){
            alert('필수항목을 입력해주세요');
            return;
        }
        /** 새로운 책, quote 객체 생성 후 db 업데이트 */

        const today = new Date();

        const newBook = {
            id:Date.now(),
            title:title,
            author:author,
            publisher:publisher || null
        }
        const newQuote ={
            id:Date.now(),
            user_id:user.id,
            source_type: 0, /**book */
            source_id : newBook.id,
            content:content,
            createdAt: today.getFullYear() + (today.getMonth()+1)+ today.getDay() + today.getHours() + today.getMinutes() + today.getMilliseconds(),
            tags:selectedTags,
            wrtier:user.id
        }
        return newBook,newQuote;
    }

    return(
        <>
        <Form className="flex flex-col mt-10">
            <div className="text-3xl mb-5">New Book Write</div>
            <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pb-2">책 제목 <span className="text-red-700">*</span></label>
                <input type="text" className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green" placeholder="책 제목을 입력하세요" value={title} onChange={e=>setTitle(e.target.value)} />
            </div>
            <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pb-2">저자 <span className="text-red-700">*</span></label>
                <input type="text" className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green" placeholder="저자를 입력하세요" value={author} onChange={e=>setAuthor(e.target.value)} />
            </div>
            <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pr-2 pb-2">출판사</label>
                <input type="text"className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green" placeholder="출판사를 입력하세요" value={publisher} onChange={e=>setPublisher(e.target.value)} />
            </div>
            <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pb-20">기록 하고싶은 문장 <span className="text-red-700">*</span>
                <div className="text-xs mr-4 text-gray-700">{charNum}/1000</div></label>
                <textarea maxLength="1000" className="w-4/6 h-32 outline-1 pb-20 pl-4 rounded-lg p-2 shadow-lg ml-3 shadow-gray-400 outline-main-green" placeholder="기록 하고싶은 문장을 입력하세요" value={content} onChange={e=>{setContent(e.target.value); setCharNum(e.target.value.length);}} />
            </div>
             <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pb-24 pr-2">태그 </label>
                <div className="w-4/6 border rounded-lg p-2 shadow-lg shadow-gray-400 ml-3 border-main-green" >
                    {tags.map((id)=>(
                        <button key={id} 
                        onClick={()=>onSelected(id)}
                        className={selectedTags.includes(id)?style[1]:style[0]}>{id}</button>
                    ))}
                </div>
            </div>
             {error&&(<div className="text-xs w-4/6 mt-4 pl-3 flex justify-center text-red-700">{error}</div>)}
             <div className="self-end">
                    <button className="rounded-xl p-2 text-xs mr-20 mt-7 w-5/12 border border-main-green hover:bg-main-pink"
                    onClick={onSubmit}>등록</button>
             </div>
        </Form>
        </>
    );
}