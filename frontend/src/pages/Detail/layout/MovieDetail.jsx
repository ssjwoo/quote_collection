import { useNavigate } from "react-router-dom";
import mark from "../../../assets/bookmark.png";
import marked from "../../../assets/bookmark_marked.png";
import { useEffect, useState } from "react";
import axios from "../../../api/axios";

export const MovieDetail = ({ quote }) => {
  const navigation = useNavigate();
  const [isLogin, setIsLogin] = useState(false);
  const [bookmark, setBookMarked] = useState(false);
  const [user, setUser] = useState({});
  const [source, setSource] = useState({});
  const [writer,setWriter] =useState({});

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
          console.log(id);
          const sourceData = await axios.get(`/source/${id}`);
          setSource(sourceData.data);
          console.log(sourceData.data);
        } catch (error) {
          console.log("Failed to get quotes_source_data", error);
        }

        if (token) {
          // TODO: /api/auth/me - need testing
          const response = await axios.get("/auth/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log("/api/auth/me", response);
          const userData = response.data;
          setUser(userData);
          setIsLogin(true);
          // Check if the current quote is bookmarked by the user
          const isBookmarked = userData.bookmarks?.some(
            (b) => b.quote_id === quote.id
          );
          setBookMarked(isBookmarked);
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

  const onIsLogin = async () => {
    if (!isLogin) {
      alert("로그인이 필요한 기능입니다.");
      return;
    }
    if (!quote || !quote.id) {
      console.error("Quote data is not available for bookmarking.");
      return;
    }

    try {
      const token = localStorage.getItem("accessToken");
      if (bookmark) {
        // Unbookmark
        // TODO: /api/bookmark/?user_id=${user.id}&quote_id=${quote.id} - need testing
        const response = await axios.delete(
          `/bookmark/?user_id=${user.id}&quote_id=${quote.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        console.log(
          `/api/bookmark/?user_id=${user.id}&quote_id=${quote.id}`,
          response
        );
        setBookMarked(false);
      } else {
        // Bookmark
        try {
          const response = await axios.post(
            "/bookmark/",
            { user_id: user.id, quote_id: quote.id },
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            }
          );
          console.log("/api/bookmark/", response);
          setBookMarked(true);
        } catch (error) {
          console.error("Failed to update bookmark:", error);
          if (error.response && error.response.status === 500) {
            // If a 500 error occurs on POST, assume it's a duplicate and try to DELETE
            try {
              const deleteResponse = await axios.delete(
                `/bookmark/?user_id=${user.id}&quote_id=${quote.id}`,
                {
                  headers: {
                    Authorization: `Bearer ${token}`,
                  },
                }
              );
              console.log(
                "Attempted to delete duplicate bookmark:",
                deleteResponse
              );
              setBookMarked(false); // Now it's unbookmarked
              alert("북마크 상태가 동기화되었습니다. 북마크를 해제했습니다.");
            } catch (deleteError) {
              console.error(
                "Failed to delete bookmark after duplicate POST:",
                deleteError
              );
              alert("북마크 상태 동기화에 실패했습니다.");
            }
          } else {
            alert("북마크 추가에 실패했습니다.");
          }
        }
      }
    } catch (error) {
      console.error("Failed to update bookmark:", error);
    }
  };
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
      await axios.delete(`/quote/${quote.id}`);
      await axios.delete(`/source/${source.id}`);

      alert("Movie deleted successfully!");
      navigation("/movie"); 
    } catch (error) {
      console.error("Error deleting Movie:", error);
      alert("Failed to delete Movie.");
    }
  };

  return (
    <>
      <div className="flex flex-col mt-10">
        <div className="text-3xl mb-5">MOVIE MOMENT</div>
        <div className="text-end">
         <label className="text-xs text-end font-semibold text-gray-600">작성자 : <span> {writer.username} </span></label>
        {/* 글 작성자에게만 보이도록 */}
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
          <label className="w-1/12 text-sm text-end pb-3">영화 제목 </label>
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
          <div className="flex p-3 mr-14">
            <img
              className="size-5 cursor-pointer"
              onClick={onIsLogin}
              src={isLogin && bookmark ? marked : mark}
            />
          </div>
        </div>
        <div className="flex items-end mt-3">
          <label className="w-1/12 text-end pb-3 text-sm">감독 </label>
          <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
            <span
              className="cursor-pointer"
              onClick={() => onSearchList(source.creator)}
            >
              {source.creator}
            </span>
          </div>
        </div>

        {(source.release_year !== 0 && source.release_year )&& (
          <>
            <div className="flex items-end mt-3">
              <label className="w-1/12 text-end pb-3 text-sm">개봉일 </label>
              <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
                {source.release_year}
              </div>
            </div>
          </>
        )}

        {/* tag 조회 */}
        {quote.tags && (
          <div className="flex items-end mt-3">
            <label className="w-1/12 text-end pb-3 text-sm">TAGS </label>
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
