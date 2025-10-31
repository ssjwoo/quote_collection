import { useEffect, useState } from "react";
import { Form, useNavigate} from "react-router-dom";
import axios from "../../../api/axios";

export const BookModi = ({ quote, source }) => {
  const navigate = useNavigate();
  const [modiQuote, setModiQuote] = useState({});

  const tags = [
    "사랑",
    "이별",
    "그리움",
    "설렘",
    "추억",
    "희망",
    "용기",
    "성장",
    "변화",
    "새로움",
    "고독",
    "불안",
    "혼란",
    "상처",
    "치유",
    "평온",
    "잔잔함",
    "빛",
    "어둠",
    "자유",
    "꿈",
    "여행",
    "일상",
    "철학",
  ];

  const [selectedTags, setSelectedTags] = useState([]); 
  const [error, setError] = useState("");
  const [charNum, setCharNum] = useState(quote.content.length);

  /** tag 선택, 미선택 스타일 변경 */
  const style = [
    "rounded-xl p-2 bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border",
    "rounded-xl p-2 bg-main-pink text-xs ml-1 mr-1 mb-1 border-main-green border",
  ];

  useEffect(()=>{
    const getPublisher = async() =>{
      try{
        const publisherData = await axios.get(`/publisher/${source.publisher_id}`);
        setModiQuote({
        title: source.title,
        author: source.creator,
        publisher: publisherData.data.name,
        content: quote.content,
      })
      }catch(e){
        console.log("Failed to get Publisher data", e);
      }
    }

    getPublisher();
  },[]);

  useEffect(() => {
    if (selectedTags.length < 5) setError("");
  }, [selectedTags]);

useEffect(() => {
  if (quote?.tags) {
    const tagsData = quote.tags.map(tag =>
      typeof tag === "object" ? tag.name : tag.id
    );
    setSelectedTags(tagsData);
  }
}, [quote]);

  const onSelected = (id) => {
  setSelectedTags((prevSelected) => {
    const isSelected = prevSelected.includes(id);

    if (isSelected) {
      return prevSelected.filter((tid) => tid !== id);
    } else {
      if (prevSelected.length >= 5) {
        setError("태그 선택은 최대 5개까지만 가능합니다.");
        return prevSelected;
      }
      return [...prevSelected, id];
    }
  });
};

   const onUpdate = async () => {
     if (
      !modiQuote.title.trim() ||
      !modiQuote.author.trim() ||
      !modiQuote.content.trim()
    ) {
      alert("필수항목을 입력해주세요");
      return;
    }

    try {
      await axios.put(`/publisher/${source.publisher_id}`, {
          name: modiQuote.publisher,
        });

      await axios.put(`/source/${source.id}`, {
        title: modiQuote.title,
        source_type: "book",
        creator: modiQuote.author,
        publisher_id: source.publisher_id,
      });

      await axios.put(`/quote/${quote.id}`, {
        content: modiQuote.content,
        source_id: quote.source_id,
        user_id: quote.user_id,
        tags: selectedTags,
      });

      alert("book update successfully!");
      navigate("/");
    } catch (error) {
      console.error("API call error:", error);
      alert(`등록 중 오류가 발생했습니다: ${error.message}`);
    }
  };

  const onDelete = async () => {
    try {
      // TODO: /api/book/${id}, navigate to "/"
      const responseQ = await axios.delete(`/quote/${quote.id}`);
      console.log(`/quote/${quote.id}`, responseQ);
      const responseS = await axios.delete(`/source/${source.id}`);
      console.log(`/source/${source.id}`, responseS);

      alert("Book deleted successfully!");
      navigate("/"); // Redirect to home or a suitable page after deletion
    } catch (error) {
      console.error("Error deleting book:", error);
      alert("Failed to delete book.");
    }
  };

  return (
    <>
      <Form className="flex flex-col mt-10">
        <div className="text-3xl mb-5">MoDIFY Book MoMENT</div>
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pb-2">
            책 제목 <span className="text-red-700">*</span>
          </label>
          <input
            type="text"
            className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green"
            placeholder="책 제목을 입력하세요"
            value={modiQuote.title}
            onChange={(e) =>
              setModiQuote({ ...modiQuote, title: e.target.value })
            }
          />
        </div>
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pb-2">
            저자 <span className="text-red-700">*</span>
          </label>
          <input
            type="text"
            className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green"
            placeholder="저자를 입력하세요"
            value={modiQuote.author}
            onChange={(e) =>
              setModiQuote({ ...modiQuote, author: e.target.value })
            }
          />
        </div>
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pr-2 pb-2">출판사</label>
          <input
            type="text"
            className="w-4/6 outline-1 rounded-lg p-2 pl-4 shadow-lg ml-3 shadow-gray-400 outline-main-green"
            placeholder="출판사를 입력하세요"
            value={modiQuote.publisher}
            onChange={(e) =>
              setModiQuote({ ...modiQuote, publisher: e.target.value })
            }
          />
        </div>
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pb-20">
            기록 하고싶은 문장 <span className="text-red-700">*</span>
            <div className="text-xs mr-4 text-gray-700">{charNum}/1000</div>
          </label>
          <textarea
            maxLength="1000"
            className="w-4/6 h-32 outline-1 pb-20 pl-4 rounded-lg p-2 shadow-lg ml-3 shadow-gray-400 outline-main-green"
            placeholder="기록 하고싶은 문장을 입력하세요"
            value={modiQuote.content}
            onChange={(e) => {
              setModiQuote({ ...modiQuote, content: e.target.value });
              setCharNum(e.target.value.length);
            }}
          />
        </div>
        <div className="flex items-end mt-3">
          <label className="w-1/5 text-end pb-24 pr-2">태그 </label>
          <div className="w-4/6 border rounded-lg p-2 shadow-lg shadow-gray-400 ml-3 border-main-green">
            {tags.map((id) => (
              <button
                key={id}
                type="button"
                onClick={() => onSelected(id)}
                className={selectedTags.includes(id) ? style[1] : style[0]}
              >
                {id}
              </button>
            ))}
          </div>
        </div>
        {error && (
          <div className="text-xs w-4/6 mt-4 pl-3 flex justify-center text-red-700">
            {error}
          </div>
        )}
        <div className="self-end flex ">
          <button
            className="rounded-xl p-2 text-xs mr-2 mt-7 w-4/12 border border-main-green hover:bg-main-pink"
            onClick={onUpdate}
          >
            수정
          </button>
          <button
            className="rounded-xl p-2 text-xs mr-20 mt-7 w-4/12 border border-main-green hover:bg-main-pink"
            onClick={onDelete}
          >
            삭제
          </button>
        </div>
      </Form>
    </>
  );
};
