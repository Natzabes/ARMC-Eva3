import { useEffect, useState } from "react";
import api from "./services/api";

function App() {

  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");
  const [selectedPdf, setSelectedPdf] = useState(null);

  const loadFiles = () => {
    api.get("/api/files")
      .then(response => {
        setFiles(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  };

  const uploadFile = async () => {

    if (!selectedFile) {
      alert("Seleccione un archivo");
      return;
    }
        
    try {
  
      setMessage(
        "Subiendo archivo..."
      );

      const response = await api.post(
        "/api/upload/presigned-url",
        {
          fileName: selectedFile.name,
          fileType: selectedFile.type,
          fileSize: selectedFile.size
        }

      );
  
      const presignedUrl =
        response.data.presignedUrl;
  
      await fetch(
        presignedUrl,
        {
          method: "PUT",
          headers: {
            "Content-Type": selectedFile.type
          },
          body: selectedFile
        }
      );
  
      setMessage(
        "Archivo subido correctamente"
      );
  
      setSelectedFile(null);
  
      loadFiles();
  
    } catch (error) {
  
      console.error(error);
  
      setMessage(
        "Error al subir archivo o archivo no permitido."
      );
    }
  };

  const deleteFile = async (fileName) => {

    const confirmDelete = window.confirm(
      `¿Eliminar ${fileName}?`
    );
  
    if (!confirmDelete) {
      return;
    }
  
    try {
  
      await api.delete(
        `/api/files/${fileName}`
      );
  
      loadFiles();
  
    } catch (error) {
  
      console.error(error);
  
      alert(
        "No se pudo eliminar el archivo"
      );
    }
  };

  useEffect(() => {
    loadFiles();
  }, []);

  return (
    <div>
      <h1>ArchivaCloud P-01</h1>

      <input
        type="file"
        onChange={(e) =>
          setSelectedFile(
            e.target.files[0]
          )
        }
      />

      <button
        onClick={uploadFile}
      >
        Subir archivo
      </button>

      <p>{message}</p>

      <hr />

      <h2>Archivos</h2>

      <ul>

          {
            files.map(file => (

              <li key={file.name}>

                {file.name}

                {" "}

                <a
                  href={file.url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Abrir
                </a>

                {" "}

                {
                  file.name.toLowerCase().endsWith(".pdf") && (
                    <button
                      onClick={() =>
                        setSelectedPdf(file.url)
                      }
                    >
                      Preview
                    </button>
                  )
                }

                {" "}

                <button
                  onClick={() =>
                    deleteFile(file.name)
                  }
                >
                  Eliminar
                </button>

              </li>

            ))
          }

      </ul>

        {
          selectedPdf && (

            <div>

              <h2>Vista previa PDF</h2>

              <iframe
                src={`${selectedPdf}#page=1`}
                width="600"
                height="800"
                title="PDF Preview"
              />

            </div>
          )
        }

    </div>
  );
}

export default App;