import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/", label: "BOOK", color: "first", darkColor: "first" },
  { to: "/ai-pick", label: "AI PICK", color: "fourth", darkColor: "fourth" },
  { to: "/mypage/bookmark", label: "BOOKMARK", color: "second", darkColor: "second" },
  { to: "/trends", label: "TRENDS", color: "third", darkColor: "third" },
];

const colorVariants = {
  first: { bg: "bg-first-menu-dim", text: "text-gray-600" },
  activeFirst: { bg: "bg-first-menu-thick", text: "text-gray-800" },
  second: { bg: "bg-second-menu-dim", text: "text-gray-600" },
  activeSecond: { bg: "bg-second-menu-thick", text: "text-gray-800" },
  third: { bg: "bg-third-menu-dim", text: "text-gray-600" },
  activeThird: { bg: "bg-third-menu-thick", text: "text-gray-800" },
  fourth: { bg: "bg-fourth-menu-dim", text: "text-indigo-600" },
  activeFourth: { bg: "bg-fourth-menu-thick", text: "text-white" },
};

const NavBar = () => {
  return (
    <>
      {/* Desktop Version: Rotated Side Menu */}
      <nav className="absolute -left-14 top-24 hidden md:block">
        <ul className="space-y-4">
          {navItems.map((item, index) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                end
                style={{ transform: `translateX(${index * 4}px)` }}
                className={({ isActive }) => {
                  const variant = isActive
                    ? colorVariants[
                    `active${item.darkColor.charAt(0).toUpperCase() +
                    item.darkColor.slice(1)
                    }`
                    ]
                    : colorVariants[item.color];
                  return (
                    `relative block w-26 h-14 my-16 py-3 px-2 text-center font-bold shadow-lg transition-transform duration-200 ease-in-out rounded-lg ` +
                    ` -rotate-90 text-sm ` +
                    `${variant.bg} ${variant.text} ` +
                    (isActive ? "z-20 scale-105" : "z-0")
                  );
                }}
              >
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Mobile Version: Bottom Tab Bar */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 md:hidden pb-safe">
        <ul className="flex justify-around items-center h-16">
          {navItems.map((item) => (
            <li key={item.to} className="flex-1 h-full">
              <NavLink
                to={item.to}
                end
                className={({ isActive }) =>
                  `flex flex-col items-center justify-center h-full text-[10px] font-bold transition-colors duration-200 ` +
                  (isActive ? "text-main-green bg-gray-50" : "text-gray-400")
                }
              >
                <span className={`w-8 h-1 mb-1 rounded-full ${colorVariants[item.color].bg} opacity-80`} />
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </>
  );
};

export default NavBar;
