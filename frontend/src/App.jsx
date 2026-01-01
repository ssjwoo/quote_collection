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
import { AuthProvider, useAuth } from "./hooks/useAuth";
import { UserProvider } from "./hooks/useUser";
import { BookmarkProvider } from "./contexts/BookmarkProvider";

const ProviderLayout = () => (
  <AuthProvider>
    <BookmarkProvider>
      <UserProvider>
        <Outlet />
      </UserProvider>
    </BookmarkProvider>
  </AuthProvider>
);

const RootLayout = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const { isLoading, isAuthenticated } = useAuth();

  useEffect(() => {
    setIsOpen(false);
  }, [location]);

  return (
    <div className="relative flex flex-nowrap justify-center bg-main-green min-h-screen">
      <div className="relative w-full flex justify-center">
        <div className="relative w-full max-w-6xl">
          <NavBar />
          <div className="relative z-10 w-full md:w-[75vw] lg:w-[65vw] mx-auto min-h-[100vh] md:min-h-[90vh] md:mt-11 bg-main-beige2 shadow-none md:shadow-2xl rounded-none md:rounded-xl overflow-hidden">
            {isOpen && (
              <div className="fixed inset-0 z-50 flex justify-center items-center bg-black/50 backdrop-blur-sm p-4">
                <LoginModal setIsOpen={setIsOpen} />
              </div>
            )}
            <MyNavBar isLogIn={isAuthenticated} setIsOpen={setIsOpen} />
            <main className="p-4 sm:p-6 md:p-12 text-center text-black pb-24 md:pb-12">
              <Logo />
              {isLoading ? (
                <div className="flex justify-center items-center min-h-[40vh]">
                  <div className="animate-pulse text-gray-500 font-medium">로딩 중...</div>
                </div>
              ) : (
                <Outlet />
              )}
            </main>
          </div>
        </div>
      </div>
    </div>
  );
};

const router = createBrowserRouter([
  {
    element: <ProviderLayout />,
    children: [
      {
        path: "/",
        element: <RootLayout />,
        children: [
          { index: true, element: <MainPage mode={"book"} /> },
          { path: "/ai-pick", element: <MainPage mode={"ai-pick"} /> },
          { path: "/trends", element: <MainPage mode={"trends"} /> },
          { path: "/write", element: <Write /> },
          { path: "/mypage/:tab", element: <Mypage /> },
          { path: "/signup", element: <Signup /> },
          { path: "/quote/:id", element: <Detail /> },
          { path: "/searchlist/:input", element: <SearchList /> },
          { path: "/bookmark", element: <BookMark /> },
          { path: "/quote/:id/modi", element: <Modify /> },
        ],
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
