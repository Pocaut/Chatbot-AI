import 'package:flutter/material.dart';
import 'package:flutter/gestures.dart';
import 'package:url_launcher/url_launcher.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatbotPage extends StatefulWidget {
  @override
  _ChatbotPageState createState() => _ChatbotPageState();
}

class _ChatbotPageState extends State<ChatbotPage> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<Map<String, String>> _messages = [];
  bool _isTyping = false;

  Future<String> _generateBotResponse(String userInput) async {
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8001/predict_intent'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'text': userInput}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final intent = data['intent'];

        final respostas = {
          "agenda": "A equipe de CS da Furia estará participando dos eventos:\n\n🏆 PGL Astana 2025 - 10/05/25 à 18/05/25\n🏆 IEM Dallas 2025 - 19/05/25 à 25/05/25\n🏆 BLAST.tv Austin Major 2025 - 03/06/25 à 22/06/25",
          "jogadores": "Nossa equipe atual conta com os titulares Molodoy, Yekindar, FalleN, KSCERATO e yuurih. Nossos reservas são o skullz e chelo.",
          "parceiros": "Atualmente os parceiros da FURIA são a Adidas, Faculdade Cruzeiro do Sul Virtual, Lenovo, Pokerstars, Redbull e Hellmann's.",
          "apoio": "Para apoiar a nossa equipe, acompanhe os jogos, compartilhe nossos posts no Instagram e X, e vista nossa marca!\nVeja produtos em: https://www.furia.gg/",
          "estatisticas": "📊 *Estatísticas da Temporada 2025*\n\n🎯 **Equipe FURIA:**\n- 54 mapas jogados\n- 23 vitórias\n- 0 empates\n- 31 derrotas\n- 3888 kills / 3845 mortes\n- 1190 rounds jogados\n- K/D ratio: 1.01\n\n👤 **Jogadores:**\n- FalleN: 54 mapas, 758 kills, 36.1% HS, 765 mortes, K/D 0.99\n- yuurih: 54 mapas, 779 kills, 48.4% HS, 742 mortes, K/D 1.05\n- Yekindar: 11 mapas, 176 kills, 58.5% HS, 168 mortes, K/D 1.05\n- KSCERATO: 54 mapas, 879 kills, 54.3% HS, 754 mortes, K/D 1.17\n- Molodoy: 67 mapas, 1187 kills, 32.9% HS, 836 mortes, K/D 1.42\n- skullz: 54 mapas, 750 kills, 57.9% HS, 761 mortes, K/D 0.99\n- chelo: 54 mapas, 722 kills, 63.2% HS, 823 mortes, K/D 0.88",
          "desconhecido": "Desculpe, não entendi sua pergunta. Pode tentar de outro jeito?"
        };

        return respostas[intent] ?? respostas["desconhecido"]!;
      } else {
        return "Erro ao se comunicar com o servidor.";
      }
    } catch (e) {
      return "Erro de conexão com o backend.";
    }
  }

  void _sendMessage(String text) async {
    if (text.trim().isEmpty) return;

    setState(() {
      _messages.add({'sender': 'user', 'text': text.trim()});
      _isTyping = true;
    });
    _controller.clear();
    _scrollDown();

    String botResponse = await _generateBotResponse(text.toLowerCase());

    setState(() {
      _messages.add({'sender': 'bot', 'text': botResponse});
      _isTyping = false;
    });
    _scrollDown();
  }

  void _scrollDown() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 400),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Widget _buildMessage(Map<String, String> message) {
    bool isUser = message['sender'] == 'user';
    bool isBot = message['sender'] == 'bot';
    String text = message['text']!;

    if (isBot && text.contains('https://')) {
      List<TextSpan> spans = [];
      RegExp exp = RegExp(r'(https?://\S+)');
      int start = 0;
      for (final match in exp.allMatches(text)) {
        if (match.start > start) {
          spans.add(TextSpan(text: text.substring(start, match.start)));
        }
        final url = match.group(0)!;
        spans.add(
          TextSpan(
            text: url,
            style: TextStyle(color: Colors.blue),
            recognizer: TapGestureRecognizer()
              ..onTap = () async {
                if (await canLaunchUrl(Uri.parse(url))) {
                  await launchUrl(Uri.parse(url));
                }
              },
          ),
        );
        start = match.end;
      }
      if (start < text.length) {
        spans.add(TextSpan(text: text.substring(start)));
      }

      return Align(
        alignment: Alignment.centerLeft,
        child: Container(
          margin: EdgeInsets.symmetric(vertical: 4, horizontal: 8),
          padding: EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: Colors.grey[300],
            borderRadius: BorderRadius.circular(12),
          ),
          child: RichText(
            text: TextSpan(
              style: TextStyle(color: Colors.black, fontSize: 16),
              children: spans,
            ),
          ),
        ),
      );
    }

    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: EdgeInsets.symmetric(vertical: 4, horizontal: 8),
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isUser ? Colors.black : Colors.grey[300],
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(
          text,
          style: TextStyle(
            color: isUser ? Colors.white : Colors.black,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 2,
        title: Row(
          children: [
            Image.asset('assets/Furia_Logo_Nome.png', height: 40),
            SizedBox(width: 8),
            Text(
              'FURIA Chatbot',
              style: TextStyle(color: Colors.black),
            ),
          ],
        ),
        iconTheme: IconThemeData(color: Colors.black),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: EdgeInsets.all(8),
              itemCount: _messages.length + (_isTyping ? 1 : 0),
              itemBuilder: (context, index) {
                if (_isTyping && index == _messages.length) {
                  return Align(
                    alignment: Alignment.centerLeft,
                    child: Container(
                      margin: EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                      padding: EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.grey[300],
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        "Digitando...",
                        style: TextStyle(color: Colors.black, fontSize: 16),
                      ),
                    ),
                  );
                }
                return _buildMessage(_messages[index]);
              },
            ),
          ),
          Divider(height: 1),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 8),
            color: Colors.white,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    textInputAction: TextInputAction.send,
                    onSubmitted: (value) => _sendMessage(value),
                    decoration: InputDecoration(
                      hintText: 'Digite sua mensagem...',
                      border: InputBorder.none,
                    ),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: () => _sendMessage(_controller.text),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
