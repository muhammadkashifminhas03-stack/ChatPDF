import React, {useState} from "react";
import API from "../api";


function PDFUpload({setPdf}){

const [file,setFile]=useState(null);


const uploadPDF=async()=>{

    const formData=new FormData();

    formData.append(
        "file",
        file
    );


    const response=await API.post(
        "/upload",
        formData
    );


    setPdf(response.data.filename);

};


return(

<div>

<h2>
Upload PDF
</h2>


<input

type="file"

accept=".pdf"

onChange={(e)=>setFile(e.target.files[0])}

/>


<button onClick={uploadPDF}>
Upload
</button>


</div>

)

}


export default PDFUpload;