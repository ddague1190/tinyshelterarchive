
<ul id="myUL">
    {% recursetree projects %}
    {% if node.level == 0 %}

    {% if not node.is_leaf_node %}
    <li class="">
      <button class="collapsible">{{ node.name }}
        </button>
    {% else %}  

    <li><button href="#" class="collapsible">{{ node.name }}</button>
    {% endif %}

    {% else %}
      {% if not node.is_leaf_node %}
    <li class="">
      <button class="collapsible content {% most_recent_ancestor node %}">{{ node.name }}</button>
      {% else %}
    
      {% if node.tree_linked %}

    <li><a class="content {% most_recent_ancestor node %} tree-link" id="{{ node.name }}" href="#" >{{ node.name }}</a>

    {% else %}

    <li><button class="{% most_recent_ancestor node %} collapsible content" >{{ node.name }}</button>

        {% endif %}

      {% endif %}
      {% endif %}

      {% if not node.is_leaf_node %}
      <ul class="">
        {{ children }}
      </ul>
      {% endif %}
    </li>

    {% endrecursetree %}
  </ul>


    var coll = document.getElementsByClassName("collapsible");
  
  
  var i;
  
  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
    console.log(this.children);
      this.classList.toggle("active");
      var content = document.getElementsByClassName(this.innerHTML);
      var x;
      for (x=0; x<content.length; x++) {

    
      if (content[x].style.display == "block") {
        content[x].style.display = "none";
      } else {
        content[x].style.display = "block";
      }
    }
    });
  

  }



   <li>
                  <a class="dropdown-toggle asdf" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Vehicles by type
                  </a>
                  <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a class="dropdown-item" href="{% url 'website:vehiclebytype' 'automobile'%}">Auto</a>
                    <a class="dropdown-item" href="{% url 'website:vehiclebytype' 'bicycle'%}">Bike</a>
                    <a class="dropdown-item" href="{% url 'website:vehiclebytype' 'trailer'%}">Trailer</a>
                    <a class="dropdown-item" href="{% url 'website:vehiclebytype' 'boat'%}">Boat</a>
                    <a class="dropdown-item" href="{% url 'website:vehiclebytype' 'other'%}">Other</a>
                  </div>
              </li>
   
              <li>
                  <a class="dropdown-toggle nav-font" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Furniture by functionality
                  </a>
                  <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <a class="dropdown-item" href="{% url 'website:listfurniturebytype' 'Kitchen'%}">Kitchen</a>
                    <a class="dropdown-item" href="{% url 'website:listfurniturebytype' 'Bathroom'%}">Bathroom</a>
                    <a class="dropdown-item" href="{% url 'website:listfurniturebytype' 'Bedroom'%}">Bedroom</a>
                    <a class="dropdown-item" href="{% url 'website:listfurniturebytype' 'Utilities'%}">Utilities</a>
                    <a class="dropdown-item" href="{% url 'website:listfurniturebytype' 'Garage'%}">Garage</a>
                    <a class="dropdown-item" href="{% url 'website:listfurniturebytype' 'Workspace'%}">Workspace</a>
                  </div>
              </li>
              <li>
                <a class="dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Furniture by build technique
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                  <a class="dropdown-item" href="{% url 'website:listfurniturebytechnique' 'welding'%}">Welding</a>
                  <a class="dropdown-item" href="{% url 'website:listfurniturebytechnique' 'carpentry'%}">Carpentry</a>
                  <a class="dropdown-item" href="{% url 'website:listfurniturebytechnique' 'fiberglass'%}">Fiberglass</a>
                  <a class="dropdown-item" href="{% url 'website:listfurniturebytechnique' 'CNC'%}">CNC</a>
                  <a class="dropdown-item" href="{% url 'website:listfurniturebytechnique' 'foam'%}">Foam</a>
                  <a class="dropdown-item" href="{% url 'website:listfurniturebytechnique' 'aluminum extrusions'%}">Aluminum Extrusions</a>
                </div>

              </li>