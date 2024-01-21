from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView, Response

from openai import OpenAI

client = OpenAI(api_key="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") #본인 API키로 수정해서 실행해주세요
# Create your views here.




#chatGPT에게 채팅 요청 API
def chatGPT(prompt):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    print(completion)
    result = completion.choices[0].message.content
    return result

#chatGPT에게 그림 요청 API
def imageGPT(prompt):
    response = client.images.generate(prompt=prompt,
    n=1,
    size="256x256")
    result =response['data'][0]['url']
    return result

def index(request):
    return render(request, 'gpt/index.html')

class chat(APIView):
    def get(self, request):
        return render(request, "gpt/index.html")

    def post(self, request):
        content = request.data.get('content', None)
        completion = client.chat.completions.create(model="gpt-3.5-turbo",
                                                    messages=[{"role": "user", "content": content}])
        result = completion.choices[0].message.content
        print(result)
        return Response(result, status=200)