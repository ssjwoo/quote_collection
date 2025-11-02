import { useNavigate} from "react-router-dom";
import mark from "../../../assets/bookmark.png";
import marked from "../../../assets/bookmark_marked.png";
import { useEffect, useState } from "react";
import axios from "../../../api/axios";
import { useBookmarks } from "../../../hooks/useBookmarks";

export const BookDetail = ({ quote }) => {
  const navigation = useNavigate();
  const { isBookmarked, toggleBookmark } = useBookmarks();
  const [isLogin, setIsLogin] = useState(false);
  const [user, setUser] = useState({});
  const [source, setSource] = useState({});
  const [writer,setWriter] =useState({});
  const [publisher,setPublisher] =useState({});

  useEffect(()=>{
    window.scrollTo({
    top: 0,
    behavior: 'smooth'
    });

    const getWriter = async () =>{
      try{
        const writerData = await axios.get(`/users/${quote.user_id}`);
        setWriter(writerData.data);
      }catch(error){
        console.log("Failed to get Writer's data",error);
      }
    }

    getWriter();
  },[quote.id]);

  useEffect(() => {
    const fetchUser = async () => {
      if (!quote || !quote.source_id) return;
      try {
        const token = localStorage.getItem("accessToken");
        try {
          const id = quote.source_id;
          const sourceData = await axios.get(`/source/${id}`);
          setSource(sourceData.data);
        } catch (error) {
          console.log("Failed to get quotes_source_data", error);
        }

        if (token) {
          const response = await axios.get("/auth/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const userData = response.data;
          setUser(userData);
          setIsLogin(true);
        } else {
          setIsLogin(false);
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        setIsLogin(false);
      }
    };

    fetchUser();
  }, [isLogin, quote?.id]);

  useEffect(()=>{
    const getPublisher = async() =>{
      try{
        const publisherData = await axios.get(`/publisher/${source.publisher_id}`);
        setPublisher(publisherData.data);
      }catch(e){
        console.log("Failed to get Publisher data", e);
      }
    }

    getPublisher();
  },[source]);

  const onSearchList = (input) => {
    navigation("/searchlist/" + input);
  };

  const onModify = () => {
    if (quote?.id) {
      navigation("/quote/" + quote.id + "/modi");
    }
  };

  const onDelete = async () => {
    try {
      const responseQ = await axios.delete(`/quote/${quote.id}`);
      console.log(`/quote/${quote.id}`, responseQ);
      const responseS = await axios.delete(`/source/${source.id}`);
      console.log(`/source/${source.id}`, responseS);

      alert("Book deleted successfully!");
      navigation("/");
    } catch (error) {
      console.error("Error deleting book:", error);
      alert("Failed to delete book.");
    }
  };

  return (
    <>
      <div className="flex flex-col mt-10">
        <div className="text-3xl mb-5">BOOK MOMENT</div>
        
        <div className="text-end">
          <label className="text-xs text-end font-semibold text-gray-600 mr-3">작성자 : <span> {writer.username}</span></label>
        {isLogin && user.id == writer.id && (
          <> 
          <button
              className="px-2 py-0.5 rounded-lg border hover:bg-main-beige border-main-green text-xs mr-1"
              onClick={onModify}
            >
              수정
            </button>
            <button
              className="px-2 py-0.5 rounded-lg border hover:bg-main-beige border-main-green text-xs"
              onClick={onDelete}
            >
              삭제
            </button>
          </> 
        )}
        </div>

        <div className="flex items-end mt-3">
          <label className="w-1/12 text-sm text-end pb-3">책 제목 </label>
          <div className="w-4/6 text-start text-xl rounded-lg p-2 pl-4 ml-3">
            <span
              className="cursor-pointer"
              onClick={() => onSearchList(source.title)}
            >
              {source.title}
            </span>
          </div>
        </div>

        <div className="flex justify-center mt-3">
          <div className="w-4/5 text-main-white pt-12 pb-12 bg-main-green rounded-lg p-2 pl-4 ml-3 shadow-lg shadow-gray-400">
            {quote.content}
          </div>
        </div>

        <div className="flex justify-end mt-3">
          <div className="flex border-2 border-sub-darkgreen rounded-lg p-3 mr-14">
            <img
              className="size-5 cursor-pointer"
              onClick={() => toggleBookmark(quote)}
              src={isBookmarked(quote.id) ? marked : mark}
            />
          </div>
        </div>

        <div className="flex items-end mt-3">
          <label className="w-1/12 text-end pb-3 text-sm">저자 </label>
          <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
            <span
              className="cursor-pointer"
              onClick={() => onSearchList(source.creator)}
            >
              {source.creator}
            </span>
          </div>
        </div>

        {publisher.name && (
          <>
            <div className="flex items-end mt-3">
              <label className="w-1/12 text-end pb-3 text-sm">출판사 </label>
              <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
                {publisher.name}
              </div>
            </div>
          </> 
        )}

        {quote.tags && (
          <div className="flex items-end mt-3">
            <label className="w-1/12 text-end text-sm pb-3">TAGS </label>
            <div className="w-4/6 text-start rounded-lg p-2 pl-4 ">
              {quote.tags.map((t) => (
                <span
                  key={t.id}
                  onClick={() => onSearchList(t.name)}
                  className="rounded-xl p-2 cursor-pointer bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border"
                >
                  {t.name}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
};
