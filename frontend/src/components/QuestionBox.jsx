import React, {useState} from "react";
import API from "../api";


function QuestionBox({setAnswer}) {

    const [question,setQuestion] = useState("");


    const askQuestion = async()=>{

        try{

            const response = await API.post(
                "/ask",
                {
                    question: question
                }
            );

            setAnswer(response.data.answer);

        }
        catch(error){

            console.log(error);

        }

    };


    return (

        <div>

            <h2>Ask Question</h2>


            <input

            type="text"

            placeholder="Enter your question"

            value={question}

            onChange={(e)=>setQuestion(e.target.value)}

            />


            <button onClick={askQuestion}>
                Ask
            </button>


        </div>

    )

}


export default QuestionBox;