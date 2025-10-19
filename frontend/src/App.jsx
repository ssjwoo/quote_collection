import {
  createBrowserRouter,
  RouterProvider,
  Outlet,
  useLocation,
} from "react-router-dom";
import NavBar from "./components/NavBar";
import { MainPage } from "./pages/MainPage";
import { Bookmark } from "./pages/Bookmark";
import { Write } from "./pages/Write";
import { Mypage } from "./pages/Mypage";
import LoginModal from "./components/Modal/LoginModal";
import { useEffect, useState } from "react";
import { Signup } from "./pages/Signup";
import { MyNavBar } from "./components/MyNavBar";
import { Logo } from './components/Logo/index';

const RootLayout = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLogIn, setIsLogin] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setIsOpen(false);
  }, [location]);

  return (
    <div className="relative flex flex-nowrap">
      <div className="min-h-screen relative justify-center justify-items-center bg-main-green">
        <div className="relative">
          <NavBar />
          <div className="relative z-10 w-[60vw] min-h-[90vh] mt-11 bg-main-white shadow-2xl rounded-lg">
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
              <Logo/>
              <Outlet />
            </main>
          </div>
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
          { path: "/bookmark", element: <Bookmark /> },
          { path: "/write", element: <Write /> },
          { path: "/mypage", element: <Mypage /> },
          { path: "/signup", element: <Signup /> },
        ],
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
