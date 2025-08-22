import React, { useState } from "react";
import { Box, Button, Input, Textarea, Select } from "@chakra-ui/react";
import { uploadFile, postText } from "./api";

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [flashcards, setFlashcards] = useState("");
  const [mcqs, setMcqs] = useState("");
  const [language, setLanguage] = useState("en");
  const [qaQuestion, setQaQuestion] = useState("");
  const [qaAnswer, setQaAnswer] = useState("");

  const handleUpload = async () => {
    const data = await uploadFile(file);
    setText(data.text);
  };

  const handleSummary = async () => {
    const data = await postText("summarize", { text, language });
    setSummary(data.summary);
  };

  const handleFlashcards = async () => {
    const data = await postText("flashcards", { text, language });
    setFlashcards(data.flashcards);
  };

  const handleMcqs = async () => {
    const data = await postText("mcqs", { text, language });
    setMcqs(data.mcqs);
  };

  const handleAskQa = async () => {
    const data = await postText("rag_qa", {
      question: qaQuestion,
      context: text,
      language,
    });
    setQaAnswer(data.answer);
  };

  return (
    <Box p={5}>
      <h2>Upload Notes/PDF</h2>
      <Input type="file" onChange={e => setFile(e.target.files[0])} />
      <Button onClick={handleUpload}>Upload & Extract</Button>
      <Textarea value={text} onChange={e => setText(e.target.value)} placeholder="Extracted text here" />
      <Select value={language} onChange={e => setLanguage(e.target.value)}>
        <option value="en">English</option>
        <option value="hi">Hindi</option>
        <option value="mr">Marathi</option>
      </Select>
      <Button onClick={handleSummary}>Summarize</Button>
      <Textarea value={summary} placeholder="Summary" />
      <Button onClick={handleFlashcards}>Generate Flashcards</Button>
      <Textarea value={flashcards} placeholder="Flashcards" />
      <Button onClick={handleMcqs}>Generate MCQs</Button>
      <Textarea value={mcqs} placeholder="MCQs" />
      <h2>Ask AI Tutor</h2>
      <Input value={qaQuestion} onChange={e => setQaQuestion(e.target.value)} placeholder="Ask a question" />
      <Button onClick={handleAskQa}>Ask</Button>
      <Textarea value={qaAnswer} placeholder="Tutor's answer" />
    </Box>
  );
}

export default App;
