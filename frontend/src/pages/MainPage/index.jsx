import { useEffect, useState } from "react";
import { Search } from "../../components/Search";
import { Popular } from "./layout/Popular";
import { New } from "./layout/New";
import { Recommend } from "./layout/Recommend";

export const MainPage = ({ mode }) => {

  const [popularQuote,setPopularQuote]= useState({});
  const [newQuote, setNewQuote] = useState([]);
  const [recomQuote, setRecomQuote]=useState([]);

  /** mode에 맞게 데이터 불러오기 */
    // TODO: API call here
    /** dummy data */
    useEffect(()=>{
        const p = {'id':0,'category':0,'title':'title','creater':'author book','subData':'pub3030',
            'content':'content contentcontentcontentcontentcontent',
            'tags':['warm','hope'],
            'writer':'hana', 'createdAt':'2013-10-23'
        }
        setPopularQuote(p);

        const n = [{'id':1,'category':1,'title':'title','creater':'author book1','subData':'pub3030',
            'content':'content ffffffffffffffff',
            'tags':['warm','hope'],
            'writer':'hana', 'createdAt':'2013-10-23'
        },
      {'id':2,'category':1,'title':'title','creater':'author book2','subData':'slkdc',
            'content':'content skddkkdddkll',
            'tags':['warm','hope'],
            'writer':'hana', 'createdAt':'2013-10-23'
        },
      {'id':3,'category':1,'title':'title','creater':'author book3','subData':'sdfkdslk',
            'content':'content newnqwlmkcwmclwmelmclmdkfnsdjclsdaklmlc',
            'tags':['warm','hope'],
            'writer':'hana', 'createdAt':'2013-10-23'
        }]
        setNewQuote(n);

        const r = [{'id':4,'category':2,'title':'title','creater':'author book1','subData':'pub3030',
            'content':'content recommend contentrecommend contentrecommend contentrecommend content',
            'tags':['warm','hope'],
            'writer':'hana', 'createdAt':'2013-10-23'
        },
      {'id':5,'category':2,'title':'title','creater':'author book2','subData':'slkdc',
            'content':'content recommend contentkkrecommend contentkmfskdm',
            'tags':['warm','hope'],
            'writer':'hana', 'createdAt':'2013-10-23'
        },
      {'id':6,'category':2,'title':'title','creater':'author book3','subData':'sdfkdslk',
            'content':'content merry christmas harry',
            'tags':['warm','hope'],
            'writer':'hana', 'createdAt':'2013-10-23'
        }]
        setRecomQuote(r);
    },[]);

  return (
    <>
      <div className="flex justify-center">
        <Search/>
      </div>
      <div className="mt-12">
        
        <Popular popularQuote={popularQuote} />
        <New newQuote={newQuote} />
        <Recommend recomQuote={recomQuote}/>

      </div>
    </>
  );
};
