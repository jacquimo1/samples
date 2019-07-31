	public int solveWordProblem(String string) {
		// TODO Write an implementation for this method declaration
		List<String> strings = Arrays.asList(string.replaceAll("\\?", "").split(" "));		
		
		if(strings.contains("plus"))
		{
			return Integer.parseInt(strings.get(strings.indexOf("plus")-1)) +
					Integer.parseInt(strings.get(strings.indexOf("plus")+1));
		}
		else if(strings.contains("minus"))
		{
			return Integer.parseInt(strings.get(strings.indexOf("minus")-1)) -
					Integer.parseInt(strings.get(strings.indexOf("minus")+1));
		}
		else if(strings.contains("multiplied"))
		{
			return Integer.parseInt(strings.get(strings.indexOf("multiplied")-1)) *
					Integer.parseInt(strings.get(strings.indexOf("multiplied")+2));
		}
		else if(strings.contains("divided"))
		{
			return Integer.parseInt(strings.get(strings.indexOf("divided")-1)) /
					Integer.parseInt(strings.get(strings.indexOf("divided")+2));		}

		return 0;
	}