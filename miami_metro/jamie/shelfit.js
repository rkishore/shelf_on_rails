javascript: var d=document, 
		w=window,
		e=w.getSelection,
		k=d.getSelection,
		x=d.selection,
		s=(e?e():(k)?k():(x?x.createRange().text:0)),
		f='http://servername:serverport/shelfit',
		l=d.location,
		e=encodeURIComponent,
		l_str = String(l),
		store1 = 'express',
		store2 = 'jcrew',
		l_store_chk1 = l_str.indexOf(store1),
		l_store_chk2 = l_str.indexOf(store2),
		size_vals,
		size_idx,
		size, 
		qtity, 
		color_vals,
		color_idx,
		color, 
		img_url,
		u; 
		
	if ((l_store_chk1 != -1) || (l_store_chk2 != -1)) 
	{ 
		if (l_store_chk1 != -1)
		{
			size_vals=d.getElementsByClassName('expandMe'); 
			if (size_vals[0]==undefined)
			{
				alert('Please choose products from a valid product page');	
			}
			else
			{
				size_idx=size_vals[0].selectedIndex;
				color_idx=1; 
				if (size_idx > 0) 
				{ 
					size=size_vals[0].options[size_idx].value;
					qtity=d.getElementById('quantity').value;
					color=d.getElementsByClassName('selectedColor')[0].innerHTML;
					img_url=d.getElementById('cat-prod-flash-alt-views').childNodes[1].childNodes[0].src; 
					u=f+'?u='+e(l.href)+'&t='+'{{uid}}'+'&s='+e(size)+'&c='+e(color)+'&q='+e(qtity)+'&imgurl='+e(img_url);  
					/* alert('Store: ' + store1 + ' Size: ' + size + ', Quantity: ' + qtity + ' Color: ' + color + ' Img URL: ' + img_url); */
				}
			}
		}	 
		else if (l_store_chk2 != -1) 
		{
			size_vals=d.getElementById('sizeSelect0');
			if (size_vals==undefined)
			{
				alert('Please choose products from a valid product page');	
			}
			else
			{
				size_idx=size_vals.selectedIndex;
				if (size_idx > 0) 
				{
					size=size_vals.options[size_idx].value;
					color_vals=d.getElementById("productColor0");
					color_idx=color_vals.selectedIndex;
					if (color_idx > 0)
					{
						color=color_vals.options[color_idx].value;
						qtity=d.getElementById("qty").value;
						img_url=d.getElementsByClassName('prod_main_img')[0].childNodes[0].childNodes[0].src;
						u=f+'?u='+e(l.href)+'&t='+'{{uid}}'+'&s='+e(size)+'&c='+e(color)+'&q='+e(qtity)+'&imgurl='+e(img_url);
						/* alert('Store: ' + store1 + ' Size: ' + size + ', Quantity: ' + qtity + ' Color: ' + color + ' Img URL: ' + img_url); */
					}
				}
			}
		}
		
		if (((l_store_chk1 != -1) && (size_vals[0]!=undefined)) || ((l_store_chk2 != -1) && (size_vals!=undefined)))
		{
			if ((size_idx > 0) && (color_idx > 0))
			{
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
				if ((size_idx < 0) && (color_idx < 0))
				{
					alert('Please select size and color from the drop down list');
				}
				else if (color_idx < 0)
				{
					alert('Please select color from the drop down list');
				}
				else
				{
					alert('Please select size from the drop down list');
				}
			}
		}			 
	}
	else 
	{
		alert('Please choose items from our list of supported stores.');
	}
	void(0);
	