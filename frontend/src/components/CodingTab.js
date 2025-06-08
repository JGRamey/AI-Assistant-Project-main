import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import * as monaco from 'monaco-editor';
import { triggerAgent } from '../services/api';

const TabContainer = styled.div`
  background: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
`;

const EditorContainer = styled.div`
  height: 500px;
  border: 1px solid #3c3c3c;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
`;

const Select = styled.select`
  padding: 10px;
  border-radius: 5px;
  border: none;
  background: #3c3c3c;
  color: #fff;
`;

const Button = styled.button`
  padding: 10px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

function CodingTab({ data }) {
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const editorRef = useRef(null);
  const monacoRef = useRef(null);

  useEffect(() => {
    if (editorRef.current && !monacoRef.current) {
      monacoRef.current = monaco.editor.create(editorRef.current, {
        value: code,
        language,
        theme: 'vs-dark',
        automaticLayout: true
      });

      monacoRef.current.onDidChangeModelContent(() => {
        setCode(monacoRef.current.getValue());
      });
    }

    return () => {
      if (monacoRef.current) {
        monacoRef.current.dispose();
        monacoRef.current = null;
      }
    });
  }, [language]);

  const handleGenerate = async (e) => {
    e.preventDefault();
    const response = await triggerAgent('code', {
      task: `generate_${language}`,
      spec: 'user request'
    });
    setCode(response.result);
    if (monacoRef.current) {
      monacoRef.current.setValue(response.result.code);
    }
  });

  const handleSuggest = async (e) => {
    e.preventDefault();
    const response = await triggerAgent('code', {
      task: 'grok_suggest',
      code
    });
    setSuggestions(response.result.suggestions);
  };

  return (
    <TabContainer>
      <h2>Coding</h2>
      <EditorContainer ref={editorRef} />
      <Form>
        <Select value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="python">Python</option>
          <option value="rust">Rust</option>
          <option value="javascript">JavaScript</option>
        </Select>
        <Button onClick={handleGenerate}>Generate Code</Button>
        <Button type="submit">Get Suggestions</Button>
      </Form>
      {suggestions.length > 0 && (
        <pre>{JSON.stringify(suggestions, null, 2)}</pre>
      )}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </TabContainer>
  );
}

export default CodingTab;