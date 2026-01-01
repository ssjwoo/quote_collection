import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

export const MyNavBar = ({ setIsOpen, isLogIn }) => {
  const navigation = useNavigate();
  const { logout, setError, showAlert } = useAuth();

  const handleLogout = (e) => {
    e.preventDefault();
    logout();
  };

  const onBookmark = () => {
    if (!isLogIn) {
      // alert("로그인이 필요한 기능입니다.");
      showAlert("로그인이 필요한 기능입니다.");
    } else {
      navigation("/mypage/bookmark");
    }
  };

  const onWrite = () => {
    if (!isLogIn) {
      // alert("로그인이 필요한 기능입니다.");
      showAlert("로그인이 필요한 기능입니다.");
    } else {
      navigation("/write");
    }
  };

  return (
    <>
      <nav className="relative flex flex-row items-center justify-end w-full pr-4 md:pr-6 mt-4 md:mt-6 text-[12px] sm:text-sm z-20 text-gray-600 font-medium">
        <div className="px-2 md:px-2 cursor-pointer hover:text-gray-900 transition-colors py-1" onClick={onBookmark}>
          bookmark
        </div>
        <span className="text-gray-300 opacity-50">|</span>
        <div className="px-2 md:px-2 cursor-pointer hover:text-gray-900 transition-colors py-1" onClick={onWrite}>
          write
        </div>
        <span className="text-gray-300 opacity-50">|</span>
        {isLogIn ? (
          <>
            <NavLink className="px-2 md:px-2 cursor-pointer hover:text-gray-900 transition-colors py-1" to="/mypage/memberinfo">
              mypage
            </NavLink>
            <button
              className="ml-3 px-4 py-1.5 md:py-1 cursor-pointer border border-gray-400 rounded-full hover:bg-gray-100 transition-all active:scale-95 bg-white shadow-sm"
              onClick={handleLogout}
            >
              logout
            </button>
          </>
        ) : (
          <>
            <button
              className="ml-3 px-5 py-1.5 md:py-1 cursor-pointer bg-main-green text-white rounded-full hover:opacity-90 transition-all active:scale-95 shadow-md"
              onClick={() => { setIsOpen(true); setError(false); }}
            >
              login
            </button>
          </>
        )}
      </nav>
    </>
  );
};
