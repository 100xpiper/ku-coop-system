with open('docs/Project_Progress_Report_Final.md', 'r', encoding='utf-8') as f:
    text = f.read()

count_somchai = text.count('สมชาย ใจดี')
count_somchai_all = text.count('สมชาย')
print('count of สมชาย ใจดี:', count_somchai)
print('count of สมชาย:', count_somchai_all)

# Replace in MD
new_text = text.replace('อาจารย์ สมชาย ใจดี', 'อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ')
new_text = new_text.replace('สมชาย ใจดี', 'อาจารย์ปรวี วงศ์สวัสดิ์สุริยะ')

with open('docs/Project_Progress_Report_Final.md', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Updated docs/Project_Progress_Report_Final.md successfully!')
