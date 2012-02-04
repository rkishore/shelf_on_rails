javascript: 
	var d=document, 
	w=window,
	e=w.getSelection,
	k=d.getSelection,
	x=d.selection,
	s=(e?e():(k)?k():(x?x.createRange().text:0)),
	f='http://localhost:8000/shelfit',
	l=d.location,
	e=encodeURIComponent,
	l_str = String(l),
	store1 = "express",
	store2 = "jcrew",
	l_store_chk1 = l_str.indexOf(store1),
	l_store_chk2 = l_str.indexOf(store2);
		
	if (l_store_chk1 != -1) 
	{ 
		var select_elems=d.getElementsByClassName('expandMe'), 
			select_idx=select_elems[0].selectedIndex;
	
		if (select_idx > 0) 
		{ 
			var size=select_elems[0].options[select_idx].value, 
				qtity=d.getElementById('quantity').value,
				color=d.getElementsByClassName('selectedColor')[0].innerText,
				u=f+'?u='+e(l.href)+'&t='+5+'&s='+e(size)+'&c='+e(color)+'&q='+e(qtity);  
			alert('Store: ' + store1 + ' Size: ' + size + ', Quantity: ' + qtity + ' Color: ' + color);
		
			a=function(){
  		  		if(!w.open(u,'t','toolbar=0,resizable=1,scrollbars=1,status=1,width=1200,height=570'))
					l.href=u;
			};
			if (/Firefox/.test(navigator.userAgent)) 
				setTimeout(a, 0); 
   			else a();		
		} 
		else 
		{ 
			alert('Please select a size from the drop down list');
		} 
	} 
	else if (l_store_chk2 != -1) 
	{
		var size_vals=d.getElementById("sizeSelect0"),
			size_idx=size_vals.selectedIndex;
		
		if (size_idx > 0) 
		{
			var size=size_vals.options[size_idx].value,
				color_vals=d.getElementById("productColor0"),
				color_idx=color_vals.selectedIndex,
				color=color_vals.options[color_idx].value,
				qtity=d.getElementById("qty").value,
				u=f+'?u='+e(l.href)+'&t='+5+'&s='+e(size)+'&c='+e(color)+'&q='+e(qtity);
			alert('Store: ' + store2 + ' Size: ' + size + ', Quantity: ' + qtity + ' Color: ' + color);
			
			a=function(){
  		  		if(!w.open(u,'t','toolbar=0,resizable=1,scrollbars=1,status=1,width=1200,height=570'))
					l.href=u;
			};
			if (/Firefox/.test(navigator.userAgent)) 
				setTimeout(a, 0); 
   			else a();
		}
		else 
		{ 
			alert('Please select a size from the drop down list');
		}
	} 
	else 
	{
		alert('Store not supported');
	}
	void(0);
	