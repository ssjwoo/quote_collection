import { useNavigate } from "react-router-dom";
import mark from "../../../assets/bookmark.png";
import marked from "../../../assets/bookmark_marked.png";
import { useEffect, useState } from "react";
import axios from "../../../api/axios";
import { useBookmarks } from '../../../hooks/useBookmarks';

export const BookDetail = ({ quote }) => {
  const navigation = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [bookmark, setBookMarked] = useState(false);
  const [user, setUser] = useState({});

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("token");
        if (token) {
          // TODO: /api/auth/me - need testing
          const response = await axios.get("/api/auth/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log("/api/auth/me", response);
          const userData = response.data;
          setUser(userData);
          // Check if the current quote is bookmarked by the user
          const isBookmarked = userData.bookmarks.some(
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
  }, [isLogin, quote.id]);

<<<<<<< HEAD
  const onIsLogin = async () => {
    if (!isLogin) {
      alert("로그인이 필요한 기능입니다.");
      return;
=======
  const onIsLogin = () => {
    if (!isLogin) {
      const ok = confirm('로그인이 필요한 기능입니다. (임시) 로그인할까요?');
      if (!ok) return;
      setIsLogin(true);
      localStorage.setItem('isLogin', '1');
>>>>>>> frontend-style
    }

    try {
      const token = localStorage.getItem("token");
      if (bookmark) {
        // Unbookmark
        // TODO: /api/bookmark/?user_id=${user.id}&quote_id=${quote.id} - need testing
        const response = await axios.delete(
          `/api/bookmark/?user_id=${user.id}&quote_id=${quote.id}`,
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
        // TODO: /api/bookmark/ - need testing
        const response = await axios.post(
          "/api/bookmark/",
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
      }
    } catch (error) {
      console.error("Failed to update bookmark:", error);
    }
  };
  const onSearchList = (input) => {
    navigation("/searchlist/" + input);
  };

  const onModify = () => {
    navigation("/detail/" + quote.id + "/modi");
  };

  const onDelete = () => {
    //TODO: make delete
  };

  return (
    <>
      <div className="flex flex-col mt-10">
        <div className="text-3xl mb-5">BOOK MOMENT</div>
<<<<<<< HEAD
        {/* 글 작성자에게만 보이도록 */}
        {user.id == quote.writer && (
          <div className="text-end">
            <button
              className="px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs mr-2"
              onClick={onModify}
            >
              수정
            </button>
            <button
              className="px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs"
              onClick={onDelete}
            >
              삭제{" "}
            </button>
          </div>
        )}
        <div className="flex items-end mt-3">
          <label className="w-1/12 text-sm text-end pb-3">책 제목 </label>
          <div className="w-4/6 text-start text-xl rounded-lg p-2 pl-4 ml-3">
            <span
              className="cursor-pointer"
              onClick={() => onSearchList(quote.title)}
            >
              {quote.title}
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
              onClick={onIsLogin}
              src={isLogin && bookmark ? marked : mark}
            />
          </div>
        </div>
        <div className="flex items-end mt-3">
          <label className="w-1/12 text-end pb-3 text-sm">저자 </label>
          <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
            <span
              className="cursor-pointer"
              onClick={() => onSearchList(quote.creater)}
            >
=======

        {user.id == quote.writer && (
          <div className="text-end">
            <button
              className="px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs mr-2"
              onClick={onModify}
            >
              수정
            </button>
            <button
              className="px-4 py-2 rounded-lg border hover:bg-main-beige border-main-green text-xs"
              onClick={onDelete}
            >
              삭제
            </button>
          </div>
        )}

        <div className="flex items-end mt-3">
          <label className="w-1/12 text-sm text-end pb-3">책 제목 </label>
          <div className="w-4/6 text-start text-xl rounded-lg p-2 pl-4 ml-3">
            <span className="cursor-pointer" onClick={() => onSearchList(quote.title)}>
              {quote.title}
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
            <img className="size-5 cursor-pointer" onClick={onIsLogin} src={(isLogin&&bookmark)?marked:mark}/>
          </div>
        </div>

        <div className="flex items-end mt-3">
          <label className="w-1/12 text-end pb-3 text-sm">저자 </label>
          <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
            <span className="cursor-pointer" onClick={() => onSearchList(quote.creater)}>
>>>>>>> frontend-style
              {quote.creater}
            </span>
          </div>
        </div>

        {quote.subData && (
          <>
            <div className="flex items-end mt-3">
              <label className="w-1/12 text-end pb-3 text-sm">출판사 </label>
              <div className="w-4/6 text-start rounded-lg p-2 pl-4 ml-3 text-sm pb-3">
                {quote.subData}
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
<<<<<<< HEAD
                  key={t.id}
                  onClick={() => onSearchList(t)}
                  className="cursor-pointer rounded-xl p-2 bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border"
                >
                  {t}
=======
                  key={String(t?.id ?? t)}
                  onClick={() => onSearchList(t)}
                  className="cursor-pointer rounded-xl p-2 bg-main-beige text-xs ml-1 mr-1 mb-1 border-sub-darkbeidge border"
                >
                  {String(t?.name ?? t)}
>>>>>>> frontend-style
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
};
