from transformers import pipeline
from rake_nltk import Rake



def extract_keywords(query):
    r = Rake()
    r.extract_keywords_from_text(query)
    keywords = r.get_ranked_phrases()
    return keywords

def chunk_text(text, chunk_size):
    print(text)
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def summarize_text(texts):
    # Load a pre-trained summarization pipeline with a specific model
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    
    counter = []

    for text in texts:
        paragraphs = text.split("\n")  # Assuming paragraphs are separated by a newlines
        for paragraph in paragraphs:
            counter.append(paragraph.strip())
            
    text = "\n".join(counter)
    
    max_tokens = 1024  # BART's max token length
    chunk_size = max_tokens // 2  # Adjust chunk size to ensure it's within the limit
    
    chunks = list(chunk_text(text, chunk_size))
    summaries = []
    
    for chunk in chunks:
        summary = summarizer(chunk, max_length=100, min_length=25, do_sample=False)
        summary_text = summary[0]['summary_text']
        summaries.append(summary_text)
    
    # Combine all summaries into a single summary text
    combined_summary = ' '.join(summaries)
    # Split the combined summary into points
    points = combined_summary.split('. ')
    
    return points
    

def extract_related_passages(query, texts):
    # Step 1: Extract keywords from the query 
    keywords = extract_keywords(query)
    
    # Step 2: Find paragraphs containing keywords
    relevant_text = []
    for text in texts:
        paragraphs = text.split("\n")  # Assuming paragraphs are separated by a newlines
        for paragraph in paragraphs:
            
            
            # Check if any keyword exists in the paragraph
            for keyword in keywords:
                if keyword in paragraph:
                    
                    relevant_text.append(paragraph.strip()) # Concatenate the paragraph with a newline
                    break  # Stop checking further keywords in this paragraph
    return relevant_text





if __name__ == "__main__":
    # Example texts (replace with your actual text corpus)
    texts = [
        """
        Key lime pie, originating from the Florida Keys, is a quintessential American dessert celebrated for its unique blend of flavors and textures. This iconic pie features a luscious filling made from the juice of key limes, a smaller and more aromatic citrus fruit compared to traditional limes. Mixed with sweetened condensed milk, the tartness of the key lime juice is balanced perfectly by the creamy sweetness of the milk, creating a smooth and velvety custard-like filling.
        
        The crust of a key lime pie is typically made from graham cracker crumbs mixed with butter and sugar, providing a crunchy contrast to the silky filling. This combination of textures, from the crisp crust to the creamy filling, contributes to the pie's irresistible appeal. While some variations use a baked crust, others opt for a no-bake version that sets in the refrigerator, enhancing convenience without compromising on taste.
        
        Garnishes for key lime pie vary but often include a dollop of whipped cream or a fluffy meringue topping, adding a light and airy finish to the dessert. The pie is traditionally served chilled, which enhances its refreshing citrus flavors, making it a perfect choice for hot summer days or as a delightful conclusion to a hearty meal.
        
        Beyond its culinary appeal, key lime pie holds cultural significance in Southern cuisine and beyond, symbolizing the vibrant flavors of the American South. Its popularity has spread globally, with variations and adaptations reflecting local tastes and ingredients. Whether enjoyed in a cozy kitchen at home or savored at a seaside restaurant, key lime pie continues to captivate dessert lovers with its tangy zest and indulgent sweetness, embodying the essence of a classic American treat.

        Geometry, often regarded as the fundamental branch of mathematics dealing with shapes, sizes, and properties of space, has fascinated thinkers and mathematicians for millennia. Its profound influence spans from ancient civilizations to modern scientific and technological advancements, shaping our understanding of the physical world and beyond.
        
        At its core, geometry explores the relationships between points, lines, angles, surfaces, and solids. The ancient Greeks, particularly Euclid, laid the foundation for geometry as a deductive system based on axioms and logical reasoning. Euclid's "Elements," composed around 300 BC, remains a definitive textbook in geometry, organizing knowledge into propositions and proofs that continue to inspire mathematical reasoning.

        Geometry's applications extend far beyond abstract theorems. In architecture, it dictates the design and construction of buildings, ensuring structural integrity and aesthetic harmony. The pyramids of Egypt, the Parthenon in Greece, and modern skyscrapers all owe their form and stability to geometric principles. Similarly, in art and design, geometric shapes and patterns serve as essential elements, influencing everything from paintings to industrial design.

        Love, often regarded as a profound and complex emotion, encompasses a spectrum of experiences and expressions that shape human relationships and personal fulfillment. At its core, love involves deep affection, care, and a sense of connection towards others, whether romantically, platonically, or within families. It transcends boundaries of culture, language, and time, influencing art, literature, and philosophy throughout history.
        
        Romantic love, characterized by passion and intimacy, forms the basis of many partnerships and marriages, fostering companionship and mutual support. It involves shared experiences, emotional bonds, and a desire for mutual growth and understanding. Beyond romantic relationships, platonic love encompasses friendships built on trust, respect, and companionship, offering solace and joy in shared moments of laughter and support.
        
        Love within families nurtures bonds between parents and children, siblings, and extended relatives, providing a foundation of security and belonging. It involves unconditional acceptance, guidance, and emotional support, shaping one's sense of identity and values from an early age. This familial love extends to caregiving and nurturing roles, embodying sacrifice and devotion across generations.
        
        Moreover, love manifests in acts of kindness, compassion, and altruism towards strangers and communities, fostering empathy and solidarity in times of adversity. It inspires generosity, forgiveness, and the desire to contribute positively to society, reflecting a broader sense of interconnectedness and humanity.
        
        In conclusion, love encompasses a diverse range of emotions and relationships that enrich our lives with meaning, purpose, and resilience. It empowers individuals to forge meaningful 

        In physics and engineering, geometry plays a crucial role in understanding spatial relationships and developing models that predict natural phenomena. Albert Einstein's theory of General Relativity, for instance, relies heavily on the geometry of curved spacetime to describe gravity as the curvature caused by mass and energy.

        Advancements in computer graphics and digital imaging rely heavily on geometric algorithms. Rendering three-dimensional scenes, simulating physics in virtual environments, and even designing microchips all leverage geometric principles. Computational geometry has emerged as a specialized field, optimizing algorithms for geometric problems ranging from geometric data structures to computational biology and robotics.

        The advent of non-Euclidean geometries in the 19th century challenged traditional notions of space. Nikolai Lobachevsky and János Bolyai independently developed hyperbolic geometry, where the parallel postulate does not hold. This opened new mathematical vistas and paved the way for Einstein's revolutionary ideas in physics.

        Geometry's impact also extends into everyday life. GPS navigation systems rely on geometric principles to determine positions and routes. Cartographers use geometry to map the Earth's surface with accuracy, enabling global communication and commerce. Even sports benefit from geometric principles, whether in designing playing fields, analyzing player movements, or optimizing athletic performance.

        In education, geometry serves as a cornerstone of mathematical curriculum, teaching students logical reasoning, problem-solving skills, and spatial awareness. It encourages abstract thinking and prepares students for careers in science, technology, engineering, and mathematics (STEM).

        Moreover, geometry's influence extends into philosophy and metaphysics, where it raises questions about the nature of space, time, and existence itself. The study of fractals and chaos theory reveals hidden geometric patterns in seemingly random natural phenomena, offering new insights into complexity and order.

        In conclusion, geometry stands as a testament to human curiosity and ingenuity, shaping our understanding of the universe from ancient times to the present day. Its applications in science, art, technology, and philosophy underscore its enduring relevance and profound impact on our world. As we continue to explore new frontiers, both in physical reality and in abstract realms, geometry remains an indispensable tool for unraveling the mysteries of our existence and expanding the boundaries of human knowledge.
        
        Natural Language Processing (NLP) is a crucial sub-field of artificial intelligence (AI), focusing on teaching computers to comprehend and interact with human languages. Beyond NLP, AI encompasses various domains such as computer vision, robotics, and expert systems. Computer vision enables machines to interpret and analyze visual data, powering applications from facial recognition to autonomous vehicles. Robotics integrates AI to develop intelligent machines capable of performing tasks in manufacturing, healthcare, and exploration. Expert systems use AI to mimic human expertise, aiding in decision-making across industries like finance and healthcare.
        
        In addition to AI, data science plays a pivotal role in transforming industries through insights derived from large datasets. Data scientists leverage statistical techniques and machine learning algorithms to extract meaningful patterns and predictions from data. This interdisciplinary field intersects with AI in developing predictive models and optimizing business processes. Moreover, blockchain technology has emerged as a decentralized ledger system, revolutionizing sectors like finance, supply chain, and healthcare by ensuring transparency, security, and efficiency in transactions.
        
        Meanwhile, the Internet of Things (IoT) connects everyday objects to the internet, enabling data collection and exchange. IoT applications range from smart homes and cities to industrial automation and agriculture. These interconnected devices generate vast amounts of data, driving demand for AI-driven analytics to derive actionable insights. Moreover, quantum computing promises unprecedented computational power, potentially solving complex problems beyond the capabilities of classical computers.
        
        In conclusion, AI, encompassing NLP and other domains, continues to reshape industries and society, driving innovation across diverse fields from healthcare and finance to transportation and entertainment. As technology evolves, interdisciplinary collaboration remains essential in harnessing its full potential for addressing global challenges and advancing human progress.

        """
    ]

    # query = "give me information on key lime pie"
    # words = extract_related_passages(query, texts)
    # text = ",\n".join(words)
    # print(texts)
    # print("\n\n")
    # print(f" Related Text: {words}")
    # print("\n\n")
    print(summarize_text(texts))

    

