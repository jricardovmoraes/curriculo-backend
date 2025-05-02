import React, { useState } from 'react';
import { CloudUploadIcon } from '@heroicons/react/outline';
import axios from 'axios';

function UploadPage() {
  const [file, setFile] = useState(null);
  const [vaga, setVaga] = useState('');
  const [loading, setLoading] = useState(false);
  const [nomeArquivo, setNomeArquivo] = useState('');
  const [textoCurriculo, setTextoCurriculo] = useState('');
  const [analiseComparativa, setAnaliseComparativa] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !vaga) return alert('Por favor, selecione um arquivo e descreva a vaga.');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('vaga', vaga);

    try {
      setLoading(true);
      setTextoCurriculo('');
      setAnaliseComparativa('');
      const response = await axios.post('https://smartcv-backend.onrender.com/upload-curriculo/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setTextoCurriculo(response.data.conteudo_texto || '');
      setAnaliseComparativa(response.data.analise_openai || '');
    } catch (error) {
      console.error('Erro ao enviar currículo:', error);
      alert('Erro ao enviar currículo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-200 via-purple-200 to-pink-200 p-6">
      <form onSubmit={handleSubmit} className="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-xl animate-fadeIn">
        <h1 className="text-4xl font-extrabold text-center text-indigo-600 mb-8 tracking-tight">
          Upload de Currículo
        </h1>

        <div className="mb-6 text-center">
          <label className="block text-gray-700 mb-2 text-sm font-semibold">
            Selecione seu currículo:
          </label>
          <div className="flex items-center justify-center w-full">
            <label className="flex flex-col items-center px-4 py-6 bg-indigo-50 text-indigo-700 rounded-lg shadow-md tracking-wide uppercase border border-indigo-300 cursor-pointer hover:bg-indigo-100 transition duration-300 ease-in-out">
              <CloudUploadIcon className="w-8 h-8 mb-2" />
              <span className="text-base leading-normal">Selecione um arquivo</span>
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={(e) => {
                  setFile(e.target.files[0]);
                  setNomeArquivo(e.target.files[0]?.name || '');
                }}
                className="hidden"
              />
            </label>
          </div>
          {nomeArquivo && (
            <p className="mt-2 text-sm text-gray-600">Arquivo selecionado: {nomeArquivo}</p>
          )}
        </div>

        <div className="mb-8 text-center">
          <label className="block text-gray-700 mb-2 text-sm font-semibold">
            Descrição da vaga:
          </label>
          <textarea
            value={vaga}
            onChange={(e) => setVaga(e.target.value)}
            className="w-full p-4 border border-gray-300 rounded-lg h-36 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-400 transition"
            placeholder="Cole aqui o texto da vaga..."
          />
        </div>

        <button
          type="submit"
          className="w-full flex justify-center items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 disabled:opacity-50"
          disabled={loading}
        >
          <CloudUploadIcon className="w-5 h-5" />
          {loading ? 'Analisando currículo...' : 'Fazer Análise Comparativa do Currículo x Vaga'}
        </button>

        {loading && (
          <div className="flex justify-center mt-4">
            <svg className="animate-spin h-6 w-6 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
            </svg>
          </div>
        )}

        {textoCurriculo && (
          <div className="mt-6 p-4 bg-gray-100 rounded-lg border border-gray-300 text-sm whitespace-pre-wrap max-h-60 overflow-y-auto">
            <h2 className="font-bold mb-2 text-indigo-600">🧠 Texto extraído do currículo:</h2>
            {textoCurriculo}
          </div>
        )}

        {analiseComparativa && (
          <div className="mt-6 p-4 bg-gray-100 rounded-lg border border-gray-300 text-sm whitespace-pre-wrap max-h-60 overflow-y-auto">
            <h2 className="font-bold mb-2 text-indigo-600">📊 Análise comparativa com a vaga:</h2>
            {analiseComparativa}
          </div>
        )}
      </form>
    </div>
  );
}

export default UploadPage;
