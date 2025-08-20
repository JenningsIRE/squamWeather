(async () => {
    const delay = (ms) => new Promise(res => setTimeout(res, ms));
    const climbs = []
    const pager = document.getElementById("pager")
      while (!pager.lastChild.classList.contains('selected')) {
      climbs.push(...[...document.getElementById('results').firstChild.childNodes].map(row => {
        return { 
          href: row.firstChild.firstChild.href,
          name: row.firstChild.firstChild.innerText,
          grade: row.childNodes[1].innerText
        }
      }));
      document.getElementsByClassName('next')[0].click()
      await delay(5000); 
     }
    climbs.push(...[...document.getElementById('results').firstChild.childNodes].map(row => {
      return { 
        href: row.firstChild.firstChild.href,
        name: row.firstChild.firstChild.innerText,
        grade: row.childNodes[1].innerText
      }
    }));
  
    const results = [];
    
    
    for (let i = 0; i < climbs.length; i++) {
      const url = climbs[i].href; 
      try {
        const res = await fetch(url);
        const text = await res.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
  
        const recent = doc.querySelectorAll('.recent-sendage, .recent-sendage.climb-sends');
        const dates = [];
        recent.forEach(section => {
          section.querySelectorAll('li').forEach(li => {
            const date = li.innerText.trim().match(/\d{4}-\d{2}-\d{2}/)
            date && dates.push(date[0]);
          });
        });
  
        results.push({ ...climbs[i],  dates: [...dates] });
  
        console.log(`Fetched [${i + 1}/${climbs.length}]: ${url}`);
      } catch (err) {
        console.error(`Failed to fetch ${url}:`, err);
      }
  
      // Optional delay to be respectful to server
      await delay(500); 
    }

  
    console.log('Completed. Results:');
    console.log(results);

    // Convert to CSV string
  const csvContent = results.map(row =>
    row.dates.map(field => `${row.name.replaceAll(',', ' ')},${row.grade},"${field.replace(/"/g, '""')}"`).join('\n')
  ).join('\n');

  // Trigger download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const u = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = u;
  a.download = 'squamish-sendage.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(u);
  })();