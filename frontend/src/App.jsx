import {
  createBrowserRouter,
  RouterProvider,
  Outlet,
  useLocation,
} from "react-router-dom";
import NavBar from "./components/NavBar";
import { MainPage } from "./pages/MainPage";
import { Write } from "./pages/Write";
import { Mypage } from "./pages/Mypage";
import LoginModal from "./components/Modal/LoginModal";
import { useEffect, useState } from "react";
import { Signup } from "./pages/Signup";
import { MyNavBar } from "./components/MyNavBar";
import { Logo } from "./components/Logo/index";
import { Detail } from "./pages/Detail";
import { SearchList } from "./pages/SearchList";
import { BookMark } from "./pages/Mypage/layout/BookMark";
import { Modify } from "./pages/Modify";
import BookmarkGroup from "./pages/Mypage/layout/BookmarkGroup";
import { AuthProvider } from "./hooks/useAuth";
import { UserProvider } from "./hooks/useUser";

const RootLayout = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLogIn, setIsLogin] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setIsOpen(false);
  }, [location]);

  // 로그인 상태 확인
  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      setIsLogin(true);
    }
  }, []);

  return (
    <div className="relative flex flex-nowrap">
      <div className="min-h-screen relative justify-center justify-items-center bg-main-green">
        <div className="relative">
        <AuthProvider>
          <UserProvider>
          <NavBar />
          <div className="relative z-10 w-[60vw] min-h-[90vh] mt-11 bg-main-beige2 shadow-2xl rounded-lg">
            {isOpen && (
              <div className=" fixed inset-0 flex justify-center items-center">
                <LoginModal setIsOpen={setIsOpen} setIsLogin={setIsLogin} />
              </div>
            )}
            <MyNavBar
              setIsLogin={setIsLogin}
              isLogIn={isLogIn}
              setIsOpen={setIsOpen}
            />
            <main className="p-8 md:p-12 text-center text-black">
              <Logo />
              <Outlet />
            </main>
          </div>
            </UserProvider>
          </AuthProvider>
        </div>
      </div>
    </div>
  );
};

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <MainPage mode={"book"} /> },
      {
        element: <Outlet />,
        children: [
          { path: "/movie", element: <MainPage mode={"movie"} /> },
          { path: "/drama", element: <MainPage mode={"drama"} /> },
          { path: "/write", element: <Write /> },
          { path: "/mypage/:tab", element: <Mypage /> },
          { path: "/signup", element: <Signup /> },
          { path: "/detail/:id", element: <Detail /> },
          { path: "/searchlist/:input", element: <SearchList /> },
          { path: "/bookmark", element: <BookMark /> },
          { path: "/detail/:id/modi", element: <Modify /> },
          {path:"/mypage/bookmark/group/:folderId", element: <BookmarkGroup />}
        ],
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
