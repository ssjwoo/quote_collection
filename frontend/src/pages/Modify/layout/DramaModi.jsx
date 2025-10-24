import { useEffect, useState } from "react";
import { Form, useParams, useNavigate } from "react-router-dom";
import axios from "../../../api/axios";

export const DramaModi = ({ quote }) => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [modiQuote, setModiQuote] = useState({
    title: quote.title,
    producer: quote.creater,
    release: quote.subdata,
    content: quote.content,
  });

  const tags = [
    "로맨스",
    "공포",
    "판타지",
    "액션",
    "스릴러",
    "공상/SF",
    "코미디",
    "철학",
    "드라마",
    "다큐멘터리",
    "예능",
    "시리즈",
    "논픽션",
    "애니메이션",
    "뮤지컬",
    "히어로",
    "TV시리즈",
    "누아르",
    "사회",
    "국내",
    "해외",
  ];
  const [selectedTags, setSelectedTags] = useState(quote.tags);
  const [error, setError] = useState("");
  const [charNum, setCharNum] = useState(quote.content.length);

  /** tag 선택, 미선택 스타일 변경 */
  const style = [
    "rounded-xl p-2 bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border",
    "rounded-xl p-2 bg-main-pink text-xs ml-1 mr-1 mb-1 border-main-green border",
  ];

  useEffect(() => {
    if (selectedTags.length < 3) setError("");
  }, [selectedTags]);

  const onSelected = (id) => {
    setSelectedTags((prevSelected) => {
      if (prevSelected.includes(id)) {
        return prevSelected.filter((tid) => tid !== id);
      } else {
        if (selectedTags.length == 3) {
          setError("태그 선택은 최대 3개까지만 가능합니다.");
          return [...prevSelected];
        }
        return [...prevSelected, id];
      }
    });
  };

  const onSubmit = async (e) => {
    e.preventDefault();

    if (
      !modiQuote.title.trim() ||
      !modiQuote.producer.trim() ||
      !modiQuote.content.trim()
    ) {
      alert("필수항목을 입력해주세요");
      return;
    }

    try {
      // TODO: /api/drama/${id}, navigate to `/detail/${id}`
      const response = await axios.put(`/api/drama/${id}`, {
        title: modiQuote.title,
        producer: modiQuote.producer,
        release_date: modiQuote.release,
        content: modiQuote.content,
        tags: selectedTags,
      });
      console.log(`/api/drama/${id}`, response);

      alert("Drama updated successfully!");
      navigate(`/detail/${id}`);
    } catch (error) {
      console.error("Error updating drama:", error);
      alert("Failed to update drama.");
    }
  };

  const onDelete = async () => {
    try {
      // TODO: /api/drama/${id}, navigate to "/"
      const response = await axios.delete(`/api/drama/${id}`);
      console.log(`/api/drama/${id}`, response);

      alert("Drama deleted successfully!");
      navigate("/"); // Redirect to home or a suitable page after deletion
    } catch (error) {
      console.error("Error deleting drama:", error);
      alert("Failed to delete drama.");
    }
  };
    return(
        <>
        <Form className="flex flex-col mt-10">
            <div className="text-3xl mb-5">MoDIFY Drama MoMENT</div>
            <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pb-2">드라마 제목 <span className="text-red-700">*</span></label>
                <input type="text" className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green" placeholder="드라마 제목을 입력하세요" value={modiQuote.title} onChange={e=>setModiQuote({...modiQuote,title:e.target.value})} />
            </div>
            <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pb-2">감독 <span className="text-red-700">*</span></label>
                <input type="text" className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green" placeholder="감독 정보를 입력하세요" value={modiQuote.producer} onChange={e=>setModiQuote({...modiQuote,producer:e.target.value})} />
            </div>
            <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pr-2 pb-2">개봉일</label>
                <input type="text"className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green" placeholder="개봉일을 입력하세요" value={modiQuote.release} onChange={e=>setModiQuote({...modiQuote,release:e.target.value})} />
            </div>
            <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pb-20">기록 하고싶은 대사 <span className="text-red-700">*</span>
                <div className="text-xs mr-4 text-gray-700">{charNum}/1000</div></label>
                <textarea maxLength="1000" className="w-4/6 h-32 outline-1 pb-20 pl-4 rounded-lg p-2 shadow-lg ml-3 shadow-gray-400 outline-main-green" placeholder="기록 하고싶은 대사를 입력하세요" value={modiQuote.content} onChange={e=>{setModiQuote({...modiQuote,content:e.target.value}); setCharNum(e.target.value.length);}} />
            </div>
             <div className="flex items-end mt-3">
                <label className="w-1/5 text-end pb-16 pr-2">태그 </label>
                <div className="w-4/6 border rounded-lg p-2 shadow-lg shadow-gray-400 ml-3 border-main-green" >
                    {tags.map((id)=>(
                        <button key={id} 
                        onClick={()=>onSelected(id)}
                        className={selectedTags.includes(id)?style[1]:style[0]}>{id}</button>
                    ))}
                </div>
            </div>
             {error&&(<div className="text-xs w-4/6 mt-4 pl-3 flex justify-center text-red-700">{error}</div>)}
            <div className="self-end flex ">
                    <button className="rounded-xl p-2 text-xs mr-2 mt-7 w-4/12 border border-main-green hover:bg-main-pink"
                    onClick={onSubmit}>수정</button>
                    <button className="rounded-xl p-2 text-xs mr-20 mt-7 w-4/12 border border-main-green hover:bg-main-pink"
                    onClick={onDelete}>삭제</button>
             </div>
        </Form>
        </>
    );
}