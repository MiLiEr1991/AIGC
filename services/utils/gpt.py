from zhipuai import ZhipuAI
client = ZhipuAI(api_key="447ac829f9435b2d51b39620925b9844.bBFsAGtLwJyDgpB1")



def gpt_zhipu(prompt, model="glm-3-turbo"):

    response = client.chat.completions.create(
    model=model, # 填写需要调用的模型名称
    messages=[{"role": "user",
               "content": """学习下面参考示例改写成英文, 其中"-》"是改写符号，学习改写的风格，\
                    1. "老人的肖像" -》"Peter Pan aged 60 years old, with a black background" \
                    2. "森林中一直猫头鹰的特写" -》 "happy dreamy owl monster sitting on a tree branch, colorful glittering particles, forest background, contoured, surrealism, close up cute, detailed feathers, bioluminescence, leaves, ethereal, ice, looking in camera, sky, sleek, modern, fairytale, fantasy, by Andy Kehoe" \
                    3. "一个非洲女人的肖像" -》 "A portrait of an African American woman on a black background at night, photo realistic, ultra realistic" \
                    4. "This image showcases a bed with a safety rail installed. The rail is white and blue, and it extends from the headboard to the foot of the bed. The bed has white sheets and a blue and white striped blanket. In the background, there is a white wardrobe with two oval-shaped doors" -》 "A town square lit only by torchlight" \
                    5. "This image appears to be an advertisement or promotional material for a product. It showcases three different metal components, possibly parts of a machine or tool, with a focus on their polished and sturdy appearance. The background is dark, which makes the silver components stand out, and there are Chinese characters present, suggesting that the product might be targeted towards a Chinese-speaking audience" -》 "Black UFO in front of a rising sun at the dawn, vibrant colours, dark surroundings, photorealisti" \
                    6. "This image appears to be an advertisement or packaging for a DIY (Do It Yourself) kit to make a lantern. The lantern is decorated with vibrant and colorful designs, including cartoon-like characters and various symbols. The packaging includes a visual of the finished lantern, a list of materials required, and a price" -》"human-like octopus sitting in a recliner with a human in fish tank on his side table"
                """
                },
              {"role": "user",
               "content": "将 '{}' 按照示例改写成英文，不超过100个字".format(prompt)}
            ],
    )

    return response.choices[0].message.content

if __name__ == "__main__":

    testPrompt = """
        a cute dog
    """
    res = gpt_zhipu(prompt=testPrompt)

    print("_gpt: ", res)
