import {useState, useEffect} from "react";
import axios from "axios";
import {useMutation} from "@tanstack/react-query";

export default function Home() {
    const [data, setData] = useState("");
    const [inputText, setInputText] = useState("");
    const [text, setText] = useState("");
    const [index, setIndex] = useState(0)

    useEffect(() => {
        if (index <= data.length) {
            setTimeout(() => {
                setText(data.slice(0,index))
                setIndex(index + 1)
            }, 50)
        }else{
            setIndex(0)
        }
    }, [text, data])


    const mutation = useMutation({
        onSuccess: (data) => {
            setData(data.poem || data.news)
            console.log(data)
        },
        mutationFn: ({textType,input}) => {
            console.log(input)
            return axios.post(`http://localhost:5000/generate_${textType}`, {input_text: input}).then(response => response.data)
        }
    })

    const handleChange = (e) => {setInputText(e.target.value)}

    return (
      <>
         <div className="text-center pt-32 px-[15%] lg:px-[25%]">
             <div className="mb-12">
                 <h1 className="text-3xl font-bold text-white text-6xl mb-6">
                     The modern Shakespeare
                 </h1>
                 <p className="text-white">
                     Write an entire poem or a news article in less than a minute!
                 </p>
             </div>
             <div className="flex flex-row shadow-2xl">
                 <textarea rows="1" value={inputText} className="caret-pink-600 rounded-bl-2xl rounded-tl-2xl resize-y w-full p-2" onChange={handleChange}/>
                 <button className="bg-purple-50 text-indigo-500 text-sm p-1 ml-0.5 font-bold" onClick={()=>{mutation.mutate({textType:"poem", input:inputText})}}>{"Generate Poem"}</button>
                 <button className="bg-pink-50 text-pink-500 rounded-tr-2xl rounded-br-2xl text-sm ml-0.5 p-1 font-bold" onClick={()=>{mutation.mutate({textType:"news", input:inputText})}}>{"Generate News"}</button>
             </div>
             <div className="mt-6 text-left bg-black/30 backdrop-opacity-10 rounded-2xl p-4 mb-20 w-[100%]">
                 <h6 className="text-lg font-bold">Generated text:</h6>
                 <pre className="generated-text">
                     { mutation.isLoading? "loading..." :
                         (
                         ! data ? "No poem or news yet"
                            :
                                text
                         )}
                 </pre>
             </div>
         </div>
      </>
  )
}