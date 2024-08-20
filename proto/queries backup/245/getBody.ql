/**
 * This is an automatically generated file
 * @name Hello world
 * @kind problem
 * @problem.severity warning
 * @id java/example/hello-world
 */

 import java


 from Method method
 where method.getLocation().getFile().getBaseName() = "Tile.java" and
         method.getName() = "canMergeWith"
 select method.getBody().getLocation(), "method"