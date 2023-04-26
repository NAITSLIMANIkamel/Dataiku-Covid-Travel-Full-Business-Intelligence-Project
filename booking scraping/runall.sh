
for file in urls/*.urls
do
python3 scrape.py $file  &
done

