// DOM에서 chat-container, url-input, query-input 요소를 가져옴
const chatContainer = document.getElementById('chat-container');
const urlInput = document.getElementById('url-input');
const queryInput = document.getElementById('query-input');

// URL을 처리하는 함수 (API 요청)
async function processURL() {
    // 사용자가 입력한 URL 값을 가져옴
    const url = urlInput.value;
    
    // URL이 없으면 함수 종료
    if (!url) return;

    // 시스템 메시지를 채팅에 추가
    addMessage('System', 'Processing URL...', 'system');

    try {
        // '/process_url' 엔드포인트로 POST 요청을 보냄
        const response = await fetch('/process_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // JSON 형식으로 데이터 전송
            },
            body: JSON.stringify({ url }), // URL 데이터를 JSON으로 변환하여 전송
        });
        
        // 응답이 정상적이지 않을 경우, 오류 처리
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to process URL');
        }

        // 응답 데이터 처리 및 시스템 메시지 추가
        const data = await response.json();
        addMessage('System', data.message, 'system');
    } catch (error) {
        // 오류 발생 시 오류 메시지를 채팅에 추가
        console.error('Error in processURL:', error);
        addMessage('Error', `Failed to process URL: ${error.message}`, 'error');
    }
}

// 사용자의 질문을 처리하는 함수
async function askQuestion() {
    // 사용자가 입력한 질문을 가져옴
    const query = queryInput.value;
    
    // 질문이 없으면 함수 종료
    if (!query) return;

    // 사용자의 메시지를 채팅에 추가
    addMessage('You', query, 'user');
    
    // 입력 필드를 비움 -> 엔터 및 Ask로 질문하고 나면 입력 박스가 비워짐 
    queryInput.value = '';

    try {
        // '/query' 엔드포인트로 POST 요청을 보냄
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // JSON 형식으로 데이터 전송
            },
            body: JSON.stringify({ query }), // 질문 데이터를 JSON으로 변환하여 전송
            credentials: 'same-origin' // 동일 출처 정책 적용
        });

        // 응답 데이터 처리 및 봇의 답변 메시지 추가
        const data = await response.json();
        addMessage('Bot', data.answer, 'bot');
    } catch (error) {
        // 오류 발생 시 오류 메시지를 채팅에 추가
        console.error('Error in askQuestion:', error);
        addMessage('Error', `Failed to get answer: ${error.message}`, 'error');
    }
}

// 채팅 메시지를 추가하는 함수
function addMessage(sender, message, className) {
    // 새로운 메시지 요소를 생성
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`; // 메시지의 클래스 지정
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`; // 보낸 사람과 메시지 내용을 추가
    
    // 메시지를 채팅 컨테이너에 추가하고 자동 스크롤을 아래로 이동
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Enter 키로 질문 제출 기능 추가
queryInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        askQuestion(); // Enter 키가 눌리면 질문 제출
    }
});
